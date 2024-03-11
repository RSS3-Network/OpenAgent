"use client"; // need this to make lazy loading work. see https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading#importing-server-components

import dynamic from "next/dynamic";

import { type TabId } from "../tabs/tabs";

const AppearanceSection = dynamic(() => import("./appearance"), {
	loading: LoadingSection,
});
const WalletsSection = dynamic(() => import("./wallets"), {
	loading: LoadingSection,
});

export function TabContent({ currentTabId }: { currentTabId: TabId }) {
	if (currentTabId === "appearance") {
		return <AppearanceSection />;
	} else if (currentTabId === "wallets") {
		return <WalletsSection />;
	}
}

function LoadingSection() {
	return <>Loading...</>;
}
