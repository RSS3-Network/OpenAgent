import { AiSessionMessageToolOutputBody_Dapp } from "@/server/api/routers/ai/types/session";
import { Card, Group, Text } from "@mantine/core";

import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkDapp({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Dapp;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.platform}>
			<DappCard item={item} />
		</ShowUpItem>
	));
}

function DappCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Dapp["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Group wrap="nowrap">
				<div>
					<Text fw="bold" lineClamp={1} size="xs" title={item.platform}>
						{item.platform}
					</Text>
				</div>
			</Group>
		</Card>
	);
}
