"use client";

import { useAskAi, useAskAiStatus } from "@/lib/ai/hooks";
import { Box, Card } from "@mantine/core";
import { AnimatePresence, m } from "framer-motion";
import { useEffect, useState } from "react";

import classes from "./question-card.module.css";

export function NewSessionGuideOnboarding({
	sessionId,
}: {
	sessionId: string;
}) {
	const [show, setShow] = useState(true);

	const { ask } = useAskAi({ sessionId });

	const { status } = useAskAiStatus({ sessionId });

	useEffect(() => {
		if (status === "pending" || status === "streaming") {
			setShow(false);
		}
		// else {
		// 	setShow(true);
		// }
	}, [status]);

	const hide = () => {
		setShow(false);
	};

	return (
		<Box left="50%" pos="absolute" px="md" top="50%">
			<AnimatePresence>
				{show && (
					<Card
						animate={{ opacity: 1, scale: 1, y: 0 }}
						classNames={{ root: classes["question-card"] }}
						component={m.div}
						exit={{ opacity: 0, scale: 0.9, y: 10 }}
						initial={{ opacity: 0, scale: 0.9, y: 10 }}
						onClick={() => {
							ask({
								body: "Hello, Let's get started!",
							});
							hide();
						}}
					>
						Hello, Let&apos;s get started!
					</Card>
				)}
			</AnimatePresence>
		</Box>
	);
}
