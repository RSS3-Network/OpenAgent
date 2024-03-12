import { ActionIconCopy } from "@/components/action-icons/copy";
import { TokenBalance } from "@/components/executor/token-balance";
import { ExecutorAddressAvatar } from "@/components/executor/executor-address-avatar";
import { Card, Group, Text, rem } from "@mantine/core";

import { ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkExecutor({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Executor;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.executorId}>
			<ExecutorCard item={item} />
		</ShowUpItem>
	));
}

function ExecutorCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Executor["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Text fw="bold">Executor</Text>
			<Group wrap="nowrap">
				<ExecutorAddressAvatar
					size={rem(20)}
					executorAddress={item.executorAddress}
				/>
				<Address address={item.executorAddress} />
				<ActionIconCopy value={item.executorAddress} />
				<ActionIconExternalLink
					href={`https://hoot.it/${item.executorAddress}`}
					label="Etherscan"
				/>
			</Group>
			<Text fw="bold">Tokens</Text>
			{item.balance.map((token) => (
				<TokenBalance
					address={token.tokenAddress}
					balance={token.tokenBalance}
					decimals={token.tokenDecimal}
					imgUrl={token.tokenImageUrl}
					key={token.tokenAddress}
					name={token.tokenName}
					symbol={token.tokenSymbol}
				/>
			))}
		</Card>
	);
}
