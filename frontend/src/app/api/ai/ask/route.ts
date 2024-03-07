import { env } from "@/env.mjs";
import { AIStream, StreamingTextResponse } from "ai";
import { type NextRequest, type NextResponse } from "next/server";
import { type Session } from "next-auth";
import { Pool } from "undici";

// This is required to enable streaming
export const dynamic = "force-dynamic";

function generateUuid() {
	return crypto.randomUUID();
}

const sessionPool = new Pool(`http://localhost:3000`, {
	connections: 50,
});

export async function POST(req: NextRequest, res: NextResponse) {
	// Extract the `messages` from the body of the request
	let { body, is_onboarding, message_id, session_id } = await req.json();

	const isNewSession = session_id === "new" || !session_id;
	session_id = isNewSession ? generateUuid() : session_id;
	message_id = message_id ?? generateUuid();
	const isOnboarding = is_onboarding ?? false;

	// @ts-ignore
	const session: Session = await sessionPool
		.request({
			headers: {
				cookie: req.headers.get("cookie")!,
			},
			method: "GET",
			path: "/api/auth/session",
		})
		.then((res) => res.body.json());

	if (!session?.user) {
		throw new Error("Session not found");
	}

	const user_id = session.user.id;

	const response = await fetch(
		isOnboarding
			? `${env.API_AI_URL}/onboarding/`
			: `${env.API_AI_URL}/stream_chat/`,
		{
			body: JSON.stringify({
				body,
				message_id,
				session_id,
				type: "natural_language",
				user_id,
			}),
			headers: {
				"Content-Type": "application/json",
			},
			method: "POST",
		}
	);

	// return new Response(response.body, {
	// 	headers: {
	// 		// ...response.headers,
	// 		Connection: "keep-alive",
	// 		"Content-Encoding": "none",
	// 		"Cache-Control": "no-cache",
	// 		"Content-Type": "text/event-stream",
	// 	},
	// });

	const data = new experimental_StreamData();
	let hasSentSessionId = false;

	// Convert the response into a friendly text-stream
	const stream = AIStream(
		response,
		(data) => {
			return data;
		},
		{
			experimental_streamData: true,
			onFinal(completion) {
				// IMPORTANT! you must close StreamData manually or the response will never finish.
				data.close();
			},
			onToken: (token) => {
				if (isNewSession && !hasSentSessionId) {
					const message_id = JSON.parse(token).message_id;
					hasSentSessionId = true;
					data.append({
						body: session_id,
						message_id,
						type: "session_id",
					});
				}
				// console.log({ token });
			},
		}
	);

	// Respond with the stream
	return new StreamingTextResponse(
		stream,
		{
			headers: {
				...response.headers,
				"Cache-Control": "no-cache, no-transform",
				Connection: "keep-alive",
				"Content-Encoding": "none",
				"Content-Type": "text/event-stream",
				"X-Accel-Buffering": "no",
			},
		},
		data as any
	);
}

/**
 * A stream wrapper to send custom JSON-encoded data back to the client.
 */
class experimental_StreamData {
	private controller: TransformStreamDefaultController<Uint8Array> | null =
		null;

	// array to store appended data
	private data: object | undefined = undefined;
	private encoder = new TextEncoder();

	// closing the stream is synchronous, but we want to return a promise
	private isClosed: boolean = false;
	// in case we're doing async work
	private isClosedPromise: Promise<void> | null = null;
	private isClosedPromiseResolver: (() => void) | undefined = undefined;

	public stream: TransformStream<Uint8Array, Uint8Array>;
	constructor() {
		this.isClosedPromise = new Promise((resolve) => {
			this.isClosedPromiseResolver = resolve;
		});

		const self = this;
		this.stream = new TransformStream({
			async flush(controller) {
				// Show a warning during dev if the data stream is hanging after 3 seconds.
				const warningTimeout =
					process.env.NODE_ENV === "development"
						? setTimeout(() => {
								console.warn(
									"The data stream is hanging. Did you forget to close it with `data.close()`?"
								);
						  }, 3000)
						: null;

				await self.isClosedPromise;

				if (warningTimeout !== null) {
					clearTimeout(warningTimeout);
				}

				if (self.data) {
					const encodedData = self.encoder.encode(
						formatStreamPart("data", self.data)
					);
					controller.enqueue(encodedData);
				}
			},
			start: async (controller) => {
				self.controller = controller;
			},
			transform: async (chunk, controller) => {
				controller.enqueue(chunk);

				// add buffered data to the stream
				if (self.data) {
					const encodedData = self.encoder.encode(JSON.stringify(self.data));
					self.data = undefined;
					controller.enqueue(encodedData);
				}
			},
		});
	}

	append(value: object): void {
		if (this.isClosed) {
			throw new Error("Data Stream has already been closed.");
		}

		this.data = value;
	}

	async close(): Promise<void> {
		if (this.isClosed) {
			throw new Error("Data Stream has already been closed.");
		}

		if (!this.controller) {
			throw new Error("Stream controller is not initialized.");
		}

		this.isClosedPromiseResolver?.();
		this.isClosed = true;
	}
}

/**
 * https://github.com/vercel/ai/blob/main/packages/core/shared/stream-parts.ts#L256
 * Prepends a string with a prefix from the `StreamChunkPrefixes`, JSON-ifies it,
 * and appends a new line.
 *
 * It ensures type-safety for the part type and value.
 */
function formatStreamPart(type: "data", value: object): string {
	return `2:${JSON.stringify(value)}\n`;
}
