"use client";

import { useAskAi, useAskAiStatus } from "@/lib/ai/hooks";
import { Grid, GridCol } from "@mantine/core";
import { AnimatePresence, m } from "framer-motion";
import { type ReactNode, useEffect, useState } from "react";

import { QuestionCard } from "./question-card";

const MGridCol = m(GridCol);

export function QuestionCards({
	questions,
	sessionId,
}: {
	questions: {
		icon: any;
		plaintext: string;
		question: ReactNode;
	}[];
	sessionId: string;
}) {
	const [show, setShow] = useState(true);

	const { ask } = useAskAi({ sessionId });

	const { status } = useAskAiStatus({ sessionId });

	useEffect(() => {
		if (status === "pending" || status === "streaming") {
			setShow(false);
		} else {
			setShow(true);
		}
	}, [status]);

	const hide = () => {
		setShow(false);
	};

	return (
		<Grid align="stretch" grow gutter="xs">
			<AnimatePresence>
				{show &&
					questions.map((q, i) => {
						return (
							<MGridCol
								animate={{ opacity: 1, scale: 1, y: 0 }}
								display="flex"
								exit={{ opacity: 0, scale: 0.9, y: 10 }}
								initial={{ opacity: 0, scale: 0.9, y: 10 }}
								key={q.plaintext}
								onClick={() => {
									ask({
										body: q.plaintext,
									});
									hide();
								}}
								span={{
									lg: 4,
									md: 6,
									sm: 12,
								}}
								transition={{ delay: i * 0.1 }}
							>
								<QuestionCard icon={q.icon} question={q.question} />
							</MGridCol>
						);
					})}
			</AnimatePresence>
		</Grid>
	);
}
