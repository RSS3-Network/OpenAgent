import { AppShellSection, ScrollArea } from "@mantine/core";
import { Suspense } from "react";

import { SessionLinkNew } from "./_components/session-link-new";
import {
	SessionLinks,
	SessionLinksSkeleton,
} from "./_components/session-links";

export default async function Page({
	params,
}: {
	params: {
		id: string;
	};
}) {
	return (
		<>
			<AppShellSection>
				<SessionLinkNew />
			</AppShellSection>

			<ScrollArea my="sm">
				<Suspense fallback={<SessionLinksSkeleton />}>
					<SessionLinks />
				</Suspense>
			</ScrollArea>
		</>
	);
}
