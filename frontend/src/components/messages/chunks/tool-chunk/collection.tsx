import { Card, Group, Image, Text } from "@mantine/core";

import { ActionIconCopy, ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkCollection({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Collection;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.nft_collection_addr}>
			<CollectionCard item={item} />
		</ShowUpItem>
	));
}

function CollectionCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Collection["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Group wrap="nowrap">
				<Image
					alt="image"
					h={60}
					radius="md"
					src={item.nft_collection_image}
					w={60}
				/>

				<div>
					<Group gap="xs" wrap="nowrap">
						<Address address={item.nft_collection_addr} />
						<ActionIconCopy value={item.nft_collection_addr} />
						<ActionIconExternalLink
							href={`https://etherscan.io/token/${item.nft_collection_addr}`}
							label="View on etherscan.io"
						/>
					</Group>
					<Text
						fw="bold"
						lineClamp={1}
						size="xs"
						title={item.nft_collection_name}
					>
						{item.nft_collection_name}
					</Text>
					<Text lineClamp={1} size="xs" title={item.nft_collection_description}>
						{item.nft_collection_description}
					</Text>
				</div>
			</Group>
		</Card>
	);
}
