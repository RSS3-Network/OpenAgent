import { api } from "@/lib/trpc/client";
import { truncateAddress } from "@/lib/wagmi/utils";
import { Text, Tooltip } from "@mantine/core";
import { Suspense } from "react";

function WalletAddressFromIdDisplayWithSuspense({
	walletId,
}: {
	walletId: number;
}) {
	const [wallet] = api.wallet.wallet.useSuspenseQuery({ walletId });
	return (
		<Tooltip label={wallet.walletAddress}>
			<Text ff="monospace">{truncateAddress(wallet.walletAddress)}</Text>
		</Tooltip>
	);
}

export function WalletAddressFromIdDisplay({ walletId }: { walletId: number }) {
	return (
		<Suspense fallback={<div>0x...</div>}>
			{walletId > 0 ? (
				<WalletAddressFromIdDisplayWithSuspense walletId={walletId} />
			) : (
				<Text ff="monospace">UNKNOWN</Text>
			)}
		</Suspense>
	);
}

export function WalletAddressDisplay({
	walletAddress,
}: {
	walletAddress: `${string}.eth` | `0x${string}`;
}) {
	return (
		<Tooltip label={walletAddress}>
			<Text ff="monospace">{truncateAddress(walletAddress)}</Text>
		</Tooltip>
	);
}
