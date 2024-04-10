import { AiSessionMessageToolOutputBody_Account } from "@/server/api/routers/ai/types/session";
import { Card, Group, Image, Text } from "@mantine/core";
import { useEnsName } from "wagmi";

import { ActionIconCopy, ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkAccount({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Account;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.account_address}>
			<AddressCard item={item} />
		</ShowUpItem>
	));
}

function AddressCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Account["data"]["items"][0];
}) {
	const { data, isPending } = useEnsName({
		address: item.account_address,
	});

	return (
		<Card>
			<Group wrap="nowrap">
				<Image
					alt="avatar"
					h={60}
					radius="md"
					src={`https://cdn.stamp.fyi/avatar/${item.account_address}`}
					w={60}
				/>

				<div>
					<Group gap="xs" wrap="nowrap">
						<Address address={item.account_address} />

						<ActionIconCopy value={item.account_address} />
						<ActionIconExternalLink
							href={`https://hoot.it/${item.account_address}`}
							label="View on Hoot.it"
						/>
					</Group>
					<Text ff="monospace" size="xs" truncate w="12rem">
						{data ?? item.account_address}
					</Text>
				</div>
			</Group>
		</Card>
	);
}
