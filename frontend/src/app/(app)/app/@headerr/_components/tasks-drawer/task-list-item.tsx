import dayjs from "@/lib/dayjs";
import { Card, Group, Skeleton, Text, Tooltip } from "@mantine/core";
import {
	IconCircleCheckFilled,
	IconCircleXFilled,
	IconLoader,
	IconLoaderQuarter,
	IconZzz,
} from "@tabler/icons-react";
import { m } from "framer-motion";

import classes from "./task-list-item.module.css";
import { TaskListItemContent } from "./task-list-item-content";

export function TaskListItem({ task }: { task: AiTaskItem }) {
	return (
		<Card
			className={classes["task-list-item"]}
			component={m.div}
			layoutId={`task-list-item-${task.task_id}`}
			my="xs"
		>
			<Group justify="space-between">
				{/* status */}
				<Text component={Group} gap="xs" tt="uppercase">
					<TasksStatusIcon status={task.status} />
					<Text size="xs" span tt="uppercase">
						{task.status}
					</Text>
				</Text>

				{/* time */}
				<Tooltip
					label={
						<Text size="xs">
							CREATED:{" "}
							{dayjs(task.created_at).format("MMMM D, YYYY [at] h:mm A")}
							{task.run_at && (
								<>
									<br />
									RUN: {dayjs(task.run_at).format("MMMM D, YYYY [at] h:mm A")}
								</>
							)}
							{task.done_at && (
								<>
									<br />
									DONE: {dayjs(task.done_at).format("MMMM D, YYYY [at] h:mm A")}
								</>
							)}
						</Text>
					}
				>
					<Text size="xs">{dayjs(task.created_at).fromNow()}</Text>
				</Tooltip>
			</Group>

			<TaskListItemContent task={task} />
		</Card>
	);
}

function TasksStatusIcon({ status }: { status: AiTaskItem["status"] }) {
	if (status === "canceled") {
		return (
			<IconCircleXFilled
				className={classes["task-status-icon"]}
				data-status="canceled"
			/>
		);
	} else if (status === "done") {
		return (
			<IconCircleCheckFilled
				className={classes["task-status-icon"]}
				data-status="done"
			/>
		);
	} else if (status === "failed") {
		return (
			<IconCircleXFilled
				className={classes["task-status-icon"]}
				data-status="failed"
			/>
		);
	} else if (status === "idle") {
		return (
			<IconZzz className={classes["task-status-icon"]} data-status="idle" />
		);
	} else if (status === "pending") {
		return (
			<IconLoaderQuarter
				className={classes["task-status-icon"]}
				data-status="pending"
			/>
		);
	} else if (status === "running") {
		return (
			<IconLoader
				className={classes["task-status-icon"]}
				data-status="running"
			/>
		);
	} else {
		return <></>;
	}
}

export function TaskListItemSkeleton() {
	return <Skeleton h={150} my="xs"></Skeleton>;
}
