"use client";

import { api } from "@/lib/trpc/client";
import { Button, Skeleton, Stack, Text } from "@mantine/core";
import Link from "next/link";
import { Suspense } from "react";

import { useWalletDropdownOpened } from ".";
import { WalletDetail } from "./wallet-detail";

function WalletsDropdownWithSuspense() {
	const [wallets] = api.wallet.wallets.useSuspenseQuery();

	const { setWalletDropdownOpened } = useWalletDropdownOpened();

	if (wallets.length === 0) {
		return (
			<Stack align="center">
				<Text c="dimmed" size="xs">
					No wallets yet.
				</Text>

				<Button
					component={Link}
					href="/app/wallets/initialization"
					onClick={() => setWalletDropdownOpened(false)}
					scroll={false}
				>
					Create Wallet
				</Button>
			</Stack>
		);
	}

	return <WalletDetail walletId={wallets[0].walletId} />;
}

function WalletDropdownSkeleton() {
	return <Skeleton h={50} />;
}

export function WalletsDropdown() {
	return (
		<Suspense fallback={<WalletDropdownSkeleton />}>
			<WalletsDropdownWithSuspense />
		</Suspense>
	);
}
