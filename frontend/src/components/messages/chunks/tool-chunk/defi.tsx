import { AiSessionMessageToolOutputBody_Defi } from "@/server/api/routers/ai/types/session";
import { Card, Group, Text } from "@mantine/core";

import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkDefi({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Defi;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.platform}>
			<DefiCard item={item} />
		</ShowUpItem>
	));
}

function DefiCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Defi["data"]["items"][0];
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
