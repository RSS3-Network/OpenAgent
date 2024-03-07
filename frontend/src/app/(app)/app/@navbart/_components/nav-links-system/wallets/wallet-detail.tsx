"use client";

import { ActionIconCopy } from "@/components/action-icons/copy";
import { ActionIconExternalLink } from "@/components/action-icons/external-link";
import { TokenBalance } from "@/components/wallets/token-balance";
import { WalletAddressAvatar } from "@/components/wallets/wallet-address-avatar";
import { WalletAddressDisplay } from "@/components/wallets/wallet-address-display";
import { api } from "@/lib/trpc/client";
import { Group, Skeleton, Stack, Text, rem } from "@mantine/core";
import { Suspense } from "react";

function WalletDetailWithSuspense({ walletId }: { walletId: number }) {
	const [wallet] = api.wallet.wallet.useSuspenseQuery({ walletId });

	if (!wallet) {
		return <>NOT FOUND</>;
	}

	return (
		<Stack>
			<div>
				<Text fw="bold">Address</Text>
				<Group gap="xs">
					<WalletAddressAvatar
						size={rem(16)}
						walletAddress={wallet.walletAddress}
					/>
					<WalletAddressDisplay walletAddress={wallet.walletAddress} />
					<ActionIconCopy value={wallet.walletAddress} />
					<ActionIconExternalLink
						href={`https://hoot.it/${wallet.walletAddress}`}
						label="View on Hoot.it"
					/>
				</Group>
			</div>

			<div>
				<Text fw="bold">Balance</Text>
				{wallet.balance.map((token) => (
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
			</div>
		</Stack>
	);
}
function WalletDetailSkeleton() {
	return <Skeleton h={50} />;
}

export function WalletDetail({ walletId }: { walletId: number }) {
	return (
		<Suspense fallback={<WalletDetailSkeleton />}>
			<WalletDetailWithSuspense walletId={walletId} />
		</Suspense>
	);
}
