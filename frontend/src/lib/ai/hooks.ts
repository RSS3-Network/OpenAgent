import { isChunkTypeof } from "@/components/messages/chunks/chunk-type-extractor";
import { api } from "@/lib/trpc/client";
import { useAtomValue } from "jotai";
import { useHydrateAtoms } from "jotai/utils";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useLayoutEffect } from "react";
import { ref, useSnapshot } from "valtio";

import { createChunkDecoder } from "./decoder";
import {
	currentIdleTaskAtom,
	sessionDetailStore,
	sessionIdAtom,
} from "./stores";
import { getNewSessionHref } from "./utils";

export function useAskAi({
	body = "hi, how are you?",
	messageId,
	sessionId,
}: {
	body?: string;
	messageId?: string;
	sessionId: string;
}) {
	const searchParams = useSearchParams();
	const router = useRouter();
	const isOnboarding = searchParams.get("onboarding") === "true";

	const utils = api.useUtils();

	const scrollToBottom = useCallback(() => {
		requestAnimationFrame(() => {
			// scroll to the bottom of the chat if the messages change and the user is at the bottom
			const bottom = window.document.body.scrollHeight;
			// const isBottom = scroll.y >= bottom - window.innerHeight - 50;
			// if (isBottom) {
			window.scrollTo({ behavior: "instant", top: bottom });
			// }
			// console.log(scroll.y, bottom, isBottom);
		});
	}, []);

	useLayoutEffect(() => {
		scrollToBottom();
	}, [scrollToBottom]);

	// useEffect(() => {
	// 	// reset status
	// 	setStatus("idle");
	// }, [sessionId]);

	const ask = useCallback(
		async (
			options: {
				body?: string;
				messageId?: string;
			} = {}
		) => {
			const _body = options.body ?? body;
			const _sessionId = sessionId;
			const _messageId = options.messageId ?? messageId;

			const sessionDetail = sessionDetailStore[_sessionId];

			if (
				sessionDetail.status === "pending" ||
				sessionDetail.status === "streaming"
			) {
				return;
			}

			// remove the `?new=true` query param
			if (searchParams.get("new") === "true") {
				router.replace(`/app/sessions/${sessionId}`);
			}

			const _abortController = new AbortController();

			if (!_sessionId) {
				throw new Error("sessionId is required.");
			}

			sessionDetail.status = "pending";
			sessionDetail.abortController = ref(_abortController);

			// push the human message to the messages
			const randomFakeMessageId = crypto.randomUUID();
			const randomFakeBlockId = crypto.randomUUID();
			const randomFakeMessageId2 = crypto.randomUUID();
			sessionDetail.messages.push({
				content: [
					{
						block_id: randomFakeBlockId,
						body: _body,
						type: "natural_language",
					},
				],
				message_id: randomFakeMessageId, // we will replace this with the real message id later
				role: "human",
				send_at: new Date().toISOString(),
			});
			sessionDetail.messages.push({
				content: [],
				message_id: randomFakeMessageId2, // we will replace this with the real message id later
				role: "ai",
				send_at: new Date().toISOString(),
			});

			scrollToBottom();

			// ask the ai

			try {
				const response = await window.fetch("/api/ai/ask", {
					body: JSON.stringify({
						body: _body,
						is_onboarding: isOnboarding,
						message_id: _messageId,
						session_id: _sessionId,
					}),
					headers: {
						"Content-Type": "application/json",
					},
					method: "POST",
					signal: sessionDetail.abortController.signal,
				});

				if (!response.body) {
					sessionDetail.status = "error";
					throw new Error("The response body is empty.");
				}

				if (sessionDetail.messages.length <= 2) {
					// new session
					utils.ai.sessions.invalidate(); // invalidate the sessions query
				}

				sessionDetail.status = "streaming";

				// read the stream
				const reader = response.body.getReader();
				if (!reader) return;
				const decoder = createChunkDecoder();

				let send_at = new Date().toISOString();

				const last = sessionDetail.messages.at(-1) as AiSessionMessageForRoleAi;
				while (true) {
					const { done, value } = await reader.read();
					if (done) {
						break;
					}

					// decode and parse the chunk
					const results = decoder(value);

					console.log(results);

					for (let i = 0; i < results.length; i++) {
						const cur = results[i];
						const lastContent = last.content;

						if (cur.type === "natural_language") {
							const targetBlock = lastContent.find(
								(c) => c.block_id === cur.block_id
							);
							if (
								targetBlock &&
								isChunkTypeof(targetBlock, "natural_language")
							) {
								targetBlock.body += cur.body;
								continue;
							}
						} else if (cur.type === "session_title") {
							sessionDetail.title = cur.body;
							continue;
						} else if (cur.type === "tool") {
							// Mark newest message as still valid
							cur.body.still_valid = true;

							const targetBlock = lastContent.find(
								(c) => c.block_id === cur.block_id
							);

							if (targetBlock && isChunkTypeof(targetBlock, "tool")) {
								targetBlock.body = {
									...targetBlock.body,
									...cur.body,
								};
								continue;
							}
						} else if (cur.type === "suggested_questions") {
							cur.block_id = randomFakeBlockId;
						} else if (cur.type === "session_id") {
							// DO NOTHING
						}

						// normal case: push the chunk to the end
						lastContent.push({
							block_id: cur.block_id,
							body: cur.body,
							type: cur.type,
						});
						last.send_at = send_at;
						last.message_id = cur.message_id;
					}

					// move the suggested questions to the end
					// const last = sessionDetailStore.messages.at(
					// 	-1
					// ) as AiSessionMessageForRoleAi;
					// const sqIndex =
					// 	last.content.findIndex((c) => c.type === "suggested_questions") ?? -1;
					// if (sqIndex !== -1) {
					// 	const sq = last.content[sqIndex];
					// 	last.content.splice(sqIndex, 1);
					// 	last.content.push(sq);
					// }

					scrollToBottom();

					// The request has been aborted, stop reading the stream.
					if (!sessionDetail.abortController) {
						reader.cancel();
						break;
					}
				}
			} catch (err) {
				console.error(err);
				// Ignore abort errors as they are expected.
				if ((err as any).name === "AbortError") {
					sessionDetail.abortController = undefined;
					return null;
				}

				// if (onError && err instanceof Error) {
				// 	onError(err);
				// }

				// setError(err as Error);
			} finally {
				sessionDetail.status = "error";
			}

			// all done
			// TODO: invalidate the session messages query
		},
		[
			body,
			isOnboarding,
			messageId,
			router,
			scrollToBottom,
			searchParams,
			sessionId,
			utils.ai.sessions,
		]
	);

	const stop = useCallback(() => {
		const sessionDetail = sessionDetailStore[sessionId];
		if (
			sessionDetail.status === "pending" ||
			sessionDetail.status === "streaming"
		) {
			console.log("stop ask ai", sessionDetail.abortController);
			if (sessionDetail.abortController) {
				sessionDetail.abortController.abort();
				sessionDetail.abortController = undefined;
			}

			sessionDetail.status = "idle";
		}
	}, [sessionId]);

	return {
		ask,
		stop,
	};
}

export function useAskAiStatus({ sessionId }: { sessionId: string }) {
	const snapshot = useSnapshot(sessionDetailStore);

	return {
		status: snapshot[sessionId]?.status ?? "idle",
	};
}

export function useAiSessionTitle({ sessionId }: { sessionId: string }) {
	const snapshot = useSnapshot(sessionDetailStore);

	const setSessionTitle = (v: string) => {
		sessionDetailStore[sessionId].title = v;
	};

	return {
		sessionTitle: snapshot[sessionId]?.title ?? null,
		setSessionTitle,
	};
}

export function useAiNewSessionRouter() {
	const router = useRouter();
	const searchParams = useSearchParams();

	const pushNewSession = () => {
		router.push(getNewSessionHref());
	};

	const replaceNewSession = () => {
		router.replace(getNewSessionHref());
	};

	const pushSession = (sessionId: string) => {
		router.push(`/app/sessions/${sessionId}`);
	};

	const isNewSession = searchParams.get("new") === "true";

	return {
		isNewSession,
		pushNewSession,
		pushSession,
		replaceNewSession,
	};
}

export function useAiIsCurrentSession(sessionId: string) {
	const { id: currentSessionId } = useParams<{ id: string }>();
	const isCurrentSession = currentSessionId === sessionId;

	return {
		isCurrentSession,
	};
}

export function useCurrentSessionId() {
	const { id: currentSessionId } = useParams<{ id: string }>();

	return {
		currentSessionId,
	};
}

export function useHydrateSessionId(sessionId: string) {
	useHydrateAtoms([[sessionIdAtom, sessionId]]);

	const [data] = api.ai.sessions.detail.useSuspenseQuery({
		sessionId: sessionId!,
	});

	useEffect(() => {
		if (!sessionDetailStore[sessionId]) {
			sessionDetailStore[sessionId] = {
				messages: [],
				status: "idle",
				title: null,
			};
		}

		if (
			data &&
			data.result.messages.length > 0 &&
			sessionDetailStore[sessionId].messages.length === 0
		) {
			data.result.messages
				.slice()
				.reverse()
				.forEach((e) => {
					sessionDetailStore[sessionId].messages.push(e);
				});
			// sessionDetailStore.messages = reversedData;
			sessionDetailStore[sessionId].title = data.result.title;
		}
	}, [data, sessionId]);

	useEffect(() => {
		return () => {
			sessionDetailStore[sessionId].messages.splice(0);
			sessionDetailStore[sessionId].title = null;
		};
	}, [sessionId]);
}

export function useCurrentIdleTask() {
	const currentIdleTask = useAtomValue(currentIdleTaskAtom);

	return {
		currentIdleTask,
	};
}
