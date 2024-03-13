"use client";

import { useCurrentSessionId } from "@/lib/ai/hooks";
import { api } from "@/lib/trpc/client";
import { Center, Stack, Text } from "@mantine/core";

import { useTaskActiveTab } from "./task-list-filter";
import { TaskListItem, TaskListItemSkeleton } from "./task-list-item";

export function TasksDrawerContent() {
	const { currentSessionId } = useCurrentSessionId();

	const { activeTab } = useTaskActiveTab();

	const { data: tasks, isPending } = api.ai.tasks.all.useInfiniteQuery(
		{
			sessionId: activeTab === "current" ? currentSessionId! : undefined,
		},
		{
			getNextPageParam: (lastPage) => lastPage.nextCursor,
		}
	);

	const hasTasks = tasks?.pages.some((page) => page.result?.length > 0);

	if (!hasTasks) {
		return (
			<Center h="80vh">
				<Stack align="center">
					<Text>NO TASK</Text>
					<Text c="dimmed" size="xs">
						Try saying &ldquo;transfer 0.0001 ETH to...&rdquo;
					</Text>
				</Stack>
			</Center>
		);
	}

	return (
		<>
			{tasks?.pages.map((page) =>
				page.result?.map((task) => (
					<TaskListItem key={task.task_id} task={task} />
				))
			)}

			{isPending &&
				Array.from({ length: 5 }).map((_, i) => (
					<TaskListItemSkeleton key={i} />
				))}
		</>
	);
}
