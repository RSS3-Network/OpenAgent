"use client";

import { api } from "@/lib/trpc/client";
import { Accordion, Alert, Button, Image, Text, Title } from "@mantine/core";
import { Suspense } from "react";

export function Wallets_() {
	const [wallets] = api.wallet.wallets.useSuspenseQuery();

	const utils = api.useUtils();
	const walletCreate = api.wallet.walletCreate.useMutation({
		onSuccess: () => {
			utils.wallet.wallets.invalidate();
		},
	});

	if (wallets.length === 0) {
		return (
			<Alert title="No Wallets" variant="light" w="100%">
				<Text>
					You can still use OpenAgent without a wallet, but you won&apos;t be
					able to interact with the blockchain.
				</Text>
				<Text>Click the button below to create a wallet instantly.</Text>
				<Button
					loading={walletCreate.isPending}
					my="md"
					onClick={() => {
						walletCreate.mutate();
					}}
				>
					✨ Create Wallet
				</Button>
			</Alert>
		);
	}

	return (
		<Accordion variant="separated">
			{wallets.map((wallet) => (
				<Accordion.Item key={wallet.walletId} value={wallet.walletAddress}>
					<Accordion.Control
						icon={
							<Image
								alt="Wallet"
								height="16px"
								src={`https://cdn.stamp.fyi/avatar/${wallet.walletAddress}`}
								width="16px"
							/>
						}
					>
						{wallet.walletAddress}
					</Accordion.Control>
					<Accordion.Panel>{wallet.walletAddress}</Accordion.Panel>
				</Accordion.Item>
			))}
		</Accordion>
	);
}

export function Wallets() {
	return (
		<>
			<Title order={4} w="100%">
				Wallets
			</Title>
			<Suspense fallback={<>loading...</>}>
				<Wallets_ />
			</Suspense>
		</>
	);
}
