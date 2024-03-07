"use client";

import { useAskAi, useAskAiStatus, useCurrentIdleTask } from "@/lib/ai/hooks";
import { ActionIcon, AppShell, Loader, Textarea, Tooltip } from "@mantine/core";
import { IconPlayerStopFilled, IconSend } from "@tabler/icons-react";
import { m, useAnimationControls } from "framer-motion";
import { useCallback, useState } from "react";

import classes from "./message-box.module.css";

export function MessageBox({ sessionId }: { sessionId: string }) {
	const [value, setValue] = useState("");
	const { ask, stop } = useAskAi({
		body: value,
		sessionId,
	});

	const { status } = useAskAiStatus({ sessionId });

	const animateControls = useAnimationControls();

	const send = useCallback(
		(v: string) => {
			v = v.trim();

			if (!v || status === "pending" || status === "streaming") {
				//shake
				animateControls.start({
					transition: { duration: 1 },
					x: [0, 5, -5, 5, -5, 5, -5, 5, -5, 0],
				});
				return;
			}

			setValue("");

			ask();
		},
		[animateControls, ask, status]
	);

	const { currentIdleTask } = useCurrentIdleTask();

	return (
		<AppShell.Footer
			classNames={{
				footer: classes.footer,
			}}
			unstyled
			withBorder={false}
		>
			<m.div animate={animateControls}>
				<Tooltip
					disabled={!currentIdleTask}
					label={
						currentIdleTask
							? "Complete or cancel the current task before asking another question."
							: null
					}
				>
					<Textarea
						autoCapitalize="true"
						autoFocus
						autosize
						className="w-full grow"
						disabled={!!currentIdleTask}
						maxRows={5}
						onChange={(e) => setValue(e.currentTarget.value)}
						onKeyDown={(e) => {
							const isEnter = e.key === "Enter" || e.keyCode === 13;
							const isNotShift = !e.shiftKey;
							if (isEnter && isNotShift) {
								e.preventDefault();
								e.stopPropagation();
								setTimeout(() => {
									send(value);
								}, 20);
							}
						}}
						placeholder="Ask me anything..."
						rightSection={
							<ActionIcon
								disabled={!!currentIdleTask}
								onClick={() => send(value)}
								variant="subtle"
							>
								{status === "pending" || status === "streaming" ? (
									<IconPlayerStopFilled onClick={() => stop()} />
								) : (
									<IconSend />
								)}
							</ActionIcon>
						}
						rightSectionPointerEvents="all"
						rows={1}
						size="md"
						spellCheck
						value={value}
					></Textarea>
				</Tooltip>
			</m.div>
		</AppShell.Footer>
	);
}
