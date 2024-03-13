import { Divider, Flex } from "@mantine/core";

import { PageModal } from "../_components/page-modal";
import { TabContent } from "./_components/tab-content";
import { Tabs } from "./_components/tabs";
import { type TabId } from "./_components/tabs/tabs";

type PageProps = {
	searchParams: {
		tab?: TabId;
	};
};

export default function Page({ searchParams }: PageProps) {
	const { tab = "appearance" } = searchParams;

	return (
		<>
			<PageModal size="xl" title="Settings" withCloseButton>
				<Flex h="60vh">
					<div className="py-2">
						<Tabs currentTabId={tab} />
					</div>

					<Divider mx="md" orientation="vertical" />

					<div className="grow">
						<TabContent currentTabId={tab} />
					</div>
				</Flex>
			</PageModal>
		</>
	);
}
