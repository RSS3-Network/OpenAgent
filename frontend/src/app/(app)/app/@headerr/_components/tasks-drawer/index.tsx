import {
	DrawerBody,
	DrawerCloseButton,
	DrawerContent,
	DrawerHeader,
	DrawerOverlay,
	Group,
} from "@mantine/core";

import { TaskListFilter } from "./task-list-filter";
import { TasksDrawerContent } from "./tasks-drawer-content";
import { TasksDrawerRoot } from "./tasks-drawer-root";

export function TasksDrawer() {
	return (
		<TasksDrawerRoot>
			<DrawerOverlay />
			<DrawerContent>
				<DrawerHeader>
					<Group w="100%">
						<TaskListFilter />
						<DrawerCloseButton />
					</Group>
				</DrawerHeader>
				<DrawerBody>
					<TasksDrawerContent />
				</DrawerBody>
			</DrawerContent>
		</TasksDrawerRoot>
	);
}
