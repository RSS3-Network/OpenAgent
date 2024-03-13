"use client";

import {
	useAskAi,
	useCurrentIdleTask,
	useCurrentSessionId,
} from "@/lib/ai/hooks";
import { Button, Group } from "@mantine/core";
import { IconMessageCircleQuestion } from "@tabler/icons-react";
import { AnimatePresence, m } from "framer-motion";

import { ScrollArea } from "../basics/scroll-area";
import { ShowUpItem } from "../basics/show-up-item";

export function SuggestedQuestionsChunk({
	questions,
}: {
	questions: string[];
}) {
	const { currentSessionId } = useCurrentSessionId();
	const { ask } = useAskAi({ sessionId: currentSessionId! });
	const { currentIdleTask } = useCurrentIdleTask();

	if (!!currentIdleTask) {
		return <></>;
	}

	return (
		<div>
			<Group align="center" gap="xs" wrap="nowrap">
				<AnimatePresence>
					<m.div
						animate={{ opacity: 1, y: 0 }}
						exit={{ opacity: 0, y: 10 }}
						initial={{ opacity: 0, y: 10 }}
					>
						<IconMessageCircleQuestion />
					</m.div>
				</AnimatePresence>

				<ScrollArea>
					<Group gap="xs" py="sm" wrap="nowrap">
						<AnimatePresence>
							{questions.map((question, i) => (
								<ShowUpItem index={i} key={question}>
									<Button
										justify="flex-start"
										onClick={() => {
											ask({ body: question });
										}}
										size="xs"
										variant="outline"
									>
										{question}
									</Button>
								</ShowUpItem>
							))}
						</AnimatePresence>
					</Group>
				</ScrollArea>
			</Group>
		</div>
	);
}
