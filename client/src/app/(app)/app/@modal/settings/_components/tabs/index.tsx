"use client";

import { NavLink } from "@mantine/core";
import { useRouter } from "next/navigation";

import { type TabId, tabs } from "./tabs";

export function Tabs({ currentTabId }: { currentTabId: TabId }) {
	const router = useRouter();

	return tabs.map((tab) => {
		const href = `/app/settings?tab=${tab.id}`;
		return (
			<NavLink
				active={tab.id === currentTabId}
				key={tab.label}
				label={tab.label}
				leftSection={tab.icon}
				onClick={() => {
					router.replace(href);
				}}
			/>
		);
	});
}
