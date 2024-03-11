"use client";

import { IconLogo } from "@/components/icons";
import { api } from "@/lib/trpc/client";
import { Button, Text } from "@mantine/core";
import { IconWallet } from "@tabler/icons-react";

import { PageModal } from "../../_components/page-modal";

export function OnboardingModal() {
	const utils = api.useUtils();
	const walletCreate = api.wallet.walletCreate.useMutation();

	return (
		<PageModal closeOnClickOutside={false}>
			{({ close }) => (
				<>
					<Text my="md">
						Hi! Welcome to use <IconLogo className="align-middle" size="1rem" />{" "}
						OpenAgent.
					</Text>

					<Text my="md">
						OpenAgent can help you to manage your crypto assets and track your
						portfolio.
					</Text>

					<Text my="md">
						Let&apos;s get started by setting up your first{" "}
						<IconWallet className="align-middle" size="1rem" />
						<Text fw={700} span>
							wallet
						</Text>{" "}
						with a simple click.
					</Text>

					<Button
						fullWidth
						loading={walletCreate.isPending}
						mt="md"
						onClick={() =>
							walletCreate.mutate(undefined, {
								onSuccess: async () => {
									await utils.wallet.wallets.invalidate();
									close();
								},
							})
						}
						size="md"
					>
						Create Wallet
					</Button>

					<Button
						disabled={walletCreate.isPending}
						fullWidth
						mt="sm"
						onClick={() => close()}
						size="md"
						variant="subtle"
					>
						Do It Later
					</Button>

					<Text my="sm" size="xs">
						*You can always create a wallet later in the settings page.
					</Text>
				</>
			)}
		</PageModal>
	);
}
