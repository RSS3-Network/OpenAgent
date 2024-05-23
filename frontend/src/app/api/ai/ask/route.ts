import { env } from "@/env.mjs";
import {
	AIStream,
	type JSONValue,
	StreamingTextResponse,
	formatStreamPart,
} from "ai";
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
		.then((res) => res.body.json())
		.catch((e) => {
			console.error(e);
			throw new Error("Error while fetching session", { cause: e });
		});

	if (!session?.user) {
		throw new Error("Session not found");
	}

	const user_id = session.user.id;

	let response: Response;
	try {
		response = await fetch(
			isOnboarding
				? `${env.BACKEND_URL}/onboarding/`
				: `${env.BACKEND_URL}/stream_chat/`,
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
	} catch (e) {
		console.error(e);
		throw new Error("Error while streaming from backend", { cause: e });
	}

	// return new Response(response.body, {
	// 	headers: {
	// 		// ...response.headers,
	// 		Connection: "keep-alive",
	// 		"Content-Encoding": "none",
	// 		"Cache-Control": "no-cache",
	// 		"Content-Type": "text/event-stream",
	// 	},
	// });

	const data = new StreamData();
	let hasSentSessionId = false;

	// Convert the response into a friendly text-stream
	const stream = AIStream(
		response,
		(data) => {
			return data;
		},
		{
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
			// headers: {
			// 	...response.headers,
			// 	"Cache-Control": "no-cache, no-transform",
			// 	Connection: "keep-alive",
			// 	"Content-Encoding": "none",
			// 	"Content-Type": "text/event-stream",
			// 	"X-Accel-Buffering": "no",
			// },
		},
		data as any
	);
}

/**
 * A stream wrapper to send custom JSON-encoded data back to the client.
 */
class StreamData {
	private controller: ReadableStreamController<Uint8Array> | null = null;

	private encoder = new TextEncoder();
	private isClosed: boolean = false;

	private warningTimeout: NodeJS.Timeout | null = null;
	public stream: ReadableStream<Uint8Array>;

	constructor() {
		const self = this;

		this.stream = new ReadableStream({
			cancel: (reason) => {
				this.isClosed = true;
			},
			pull: (controller) => {
				// No-op: we don't need to do anything special on pull
			},
			start: async (controller) => {
				self.controller = controller;

				// Set a timeout to show a warning if the stream is not closed within 3 seconds
				if (process.env.NODE_ENV === "development") {
					self.warningTimeout = setTimeout(() => {
						console.warn(
							"The data stream is hanging. Did you forget to close it with `data.close()`?"
						);
					}, 3000);
				}
			},
		});
	}

	append(value: JSONValue): void {
		if (this.isClosed) {
			throw new Error("Data Stream has already been closed.");
		}

		if (!this.controller) {
			throw new Error("Stream controller is not initialized.");
		}

		this.controller.enqueue(
			this.encoder.encode(formatStreamPart("data", [value]))
		);
	}

	appendMessageAnnotation(value: JSONValue): void {
		if (this.isClosed) {
			throw new Error("Data Stream has already been closed.");
		}

		if (!this.controller) {
			throw new Error("Stream controller is not initialized.");
		}

		this.controller.enqueue(
			this.encoder.encode(formatStreamPart("message_annotations", [value]))
		);
	}

	async close(): Promise<void> {
		if (this.isClosed) {
			throw new Error("Data Stream has already been closed.");
		}

		if (!this.controller) {
			throw new Error("Stream controller is not initialized.");
		}

		this.controller.close();
		this.isClosed = true;

		// Clear the warning timeout if the stream is closed
		if (this.warningTimeout) {
			clearTimeout(this.warningTimeout);
		}
	}
}
