// TODO:
import { Text } from "@mantine/core";

export function TaskCardContent({ task }: { task: AiTaskItem }) {
	return (
		<>
			<Text>From</Text>
			<Text></Text>
			{task.created_at}
		</>
	);
}
