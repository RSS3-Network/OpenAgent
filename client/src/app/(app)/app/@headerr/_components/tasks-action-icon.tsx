"use client";

import { ActionIcon, Tooltip } from "@mantine/core";
import { IconListDetails } from "@tabler/icons-react";

import { useTasksDrawerOpened } from "./tasks-drawer/tasks-drawer-root";

export function TasksActionIcon() {
	const { setIsTasksDrawerOpened } = useTasksDrawerOpened();

	return (
		<Tooltip label="Tasks">
			<ActionIcon
				color="gray"
				onClick={() => {
					setIsTasksDrawerOpened(true);
				}}
				size="1.25rem"
				variant="light"
			>
				<IconListDetails />
			</ActionIcon>
		</Tooltip>
	);
}
