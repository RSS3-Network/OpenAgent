"use client";

import { SegmentedControl } from "@mantine/core";
import { atom, useAtom } from "jotai";

const taskActiveTabAtom = atom<"all" | "current">("current");

export function useTaskActiveTab() {
	const [activeTab, setActiveTab] = useAtom(taskActiveTabAtom);

	return {
		activeTab,
		setActiveTab,
	};
}

export function TaskListFilter() {
	const { activeTab, setActiveTab } = useTaskActiveTab();

	return (
		<SegmentedControl
			className="flex-1"
			data={[
				{ label: "Current Chat", value: "current" },
				{ label: "All", value: "all" },
			]}
			fullWidth
			onChange={(e) => setActiveTab(e as any)}
			value={activeTab}
		/>
	);
}
