import type { ReactNode } from "react";

import { Card, Group, Text } from "@mantine/core";

import classes from "./question-card.module.css";

export function QuestionCard({
	icon,
	question,
}: {
	icon: any;
	question: ReactNode;
}) {
	return (
		<Card
			classNames={{
				root: classes["question-card"],
			}}
			radius="md"
			shadow="sm"
		>
			<Group justify="center" wrap="nowrap">
				<Group className="flex-1">{icon}</Group>
				<Text size="sm">{question}</Text>
			</Group>
		</Card>
	);
}
