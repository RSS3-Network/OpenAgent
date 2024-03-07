import { ActionIconCopy } from "@/components/action-icons/copy";
import { TokenBalance } from "@/components/wallets/token-balance";
import { WalletAddressAvatar } from "@/components/wallets/wallet-address-avatar";
import { Card, Group, Text, rem } from "@mantine/core";

import { ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkWallet({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Wallet;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.walletId}>
			<WalletCard item={item} />
		</ShowUpItem>
	));
}

function WalletCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Wallet["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Text fw="bold">Wallet</Text>
			<Group wrap="nowrap">
				<WalletAddressAvatar
					size={rem(20)}
					walletAddress={item.walletAddress}
				/>
				<Address address={item.walletAddress} />
				<ActionIconCopy value={item.walletAddress} />
				<ActionIconExternalLink
					href={`https://hoot.it/${item.walletAddress}`}
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
