"use client";

import { useHydrateSessionId } from "@/lib/ai/hooks";
import { sessionDetailStore } from "@/lib/ai/stores";
import { Stack } from "@mantine/core";
import { useEffect } from "react";
import { ErrorBoundary } from "react-error-boundary";
import { useSnapshot } from "valtio";

import { Message, MessageSkeleton } from "./message";
import { FloatingTask } from "./tasks/floating-task";

export function Messages_({ sessionId }: { sessionId: string }) {
	const store = useSnapshot(sessionDetailStore);
	// const session = useSession();
	useEffect(() => {
		console.log("re-render messages list", store[sessionId]?.messages);
	});

	return (
		<Stack gap="0">
			{store[sessionId]?.messages.map((message, i) => {
				const isLastMessage = i === store[sessionId]?.messages.length - 1;

				return (
					<Message
						isLastMessage={isLastMessage}
						key={message.message_id}
						message={sessionDetailStore[sessionId]?.messages[i]}
					/>
				);
			})}
		</Stack>
	);
}

export function Messages({ sessionId }: { sessionId: string }) {
	return (
		<>
			<HydrateSessionId sessionId={sessionId} />

			<ErrorBoundary
				fallbackRender={(props) => (
					<div className="">Sorry! Something wrong.</div>
					// <div>{props.error.message + props.error.stack}</div>
				)}
			>
				<Messages_ sessionId={sessionId} />
			</ErrorBoundary>

			<FloatingTask sessionId={sessionId} />
		</>
	);
}

function HydrateSessionId({ sessionId }: { sessionId: string }) {
	useHydrateSessionId(sessionId);
	return <></>;
}

export function MessagesSkeleton() {
	return (
		<Stack gap="0">
			<MessageSkeleton role="human" />
			<MessageSkeleton role="ai" />
			<MessageSkeleton role="human" />
			<MessageSkeleton role="ai" />
			<MessageSkeleton role="human" />
			<MessageSkeleton role="ai" />
		</Stack>
	);
}
