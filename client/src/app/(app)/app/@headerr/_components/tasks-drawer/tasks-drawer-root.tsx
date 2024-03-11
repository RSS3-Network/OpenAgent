"use client";

import { DrawerRoot } from "@mantine/core";
import { atom, useAtom } from "jotai";

const tasksDrawerOpenedAtom = atom(false);

export function useTasksDrawerOpened() {
	const [isTasksDrawerOpened, setIsTasksDrawerOpened] = useAtom(
		tasksDrawerOpenedAtom
	);

	return {
		isTasksDrawerOpened,
		setIsTasksDrawerOpened,
	};
}

export function TasksDrawerRoot({ children }: { children: React.ReactNode }) {
	const { isTasksDrawerOpened, setIsTasksDrawerOpened } =
		useTasksDrawerOpened();

	return (
		<DrawerRoot
			onClose={() => setIsTasksDrawerOpened(false)}
			opened={isTasksDrawerOpened}
			position="right"
		>
			{children}
		</DrawerRoot>
	);
}
