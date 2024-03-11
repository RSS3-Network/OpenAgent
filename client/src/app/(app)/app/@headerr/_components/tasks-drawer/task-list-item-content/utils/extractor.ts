export function isTaskTypeOf<T extends AiTaskType>(
	task: AiTaskItem,
	type: T
): task is AiTaskItem<T> {
	return task.type === type;
}
