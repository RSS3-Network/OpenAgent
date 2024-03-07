"use client";

import { useAiSessionTitle } from "@/lib/ai/hooks";
import { Text } from "@mantine/core";
import { useEffect, useState } from "react";

export function SessionTitle({
	isNewChat,
	sessionId,
}: {
	isNewChat?: boolean;
	sessionId: string;
}) {
	const { sessionTitle } = useAiSessionTitle({ sessionId });
	const [typingWord, setTypingWord] = useState("");

	const title = isNewChat ? "New Chat" : sessionTitle;

	useEffect(() => {
		if (!title) return;

		if (isNewChat) {
			setTypingWord(title);
			return;
		}

		// clear first
		setTypingWord("");

		let timer: NodeJS.Timeout | null = null;

		timer = setInterval(() => {
			// set the typing word with title's letters one by one
			setTypingWord((prev) => {
				if (prev === title) {
					timer && clearInterval(timer);
					return prev;
				}
				const nextLetter = title[prev.length];
				return nextLetter ? prev + nextLetter : prev;
			});
		}, 20);

		return () => {
			timer && clearInterval(timer);
			setTypingWord("");
		};
	}, [isNewChat, title]);

	return (
		<Text fw="bold" lineClamp={1} size="lg">
			{typingWord}
		</Text>
	);
}
