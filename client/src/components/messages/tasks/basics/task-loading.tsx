import { Card, LoadingOverlay } from "@mantine/core";
import { m } from "framer-motion";

export function TaskLoading({ taskId }: { taskId: string }) {
	return (
		<Card component={m.div} h={60} layoutId={taskId} w={100}>
			<LoadingOverlay visible />
		</Card>
	);
}
