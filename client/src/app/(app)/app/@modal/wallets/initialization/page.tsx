"use client";

import { api } from "@/lib/trpc/client";
import { Anchor, Button, Flex, Portal, Text } from "@mantine/core";
import { IconWallet } from "@tabler/icons-react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useEffect, useState } from "react";

import { PageModal } from "../../_components/page-modal";

const Confetti = dynamic(() => import("react-confetti"));

export default function Page() {
	const { data: wallets, isPending } = api.wallet.wallets.useQuery();
	const utils = api.useUtils();

	const [showConfetti, setShowConfetti] = useState(false);

	const walletCreate = api.wallet.walletCreate.useMutation({
		async onSuccess() {
			await utils.wallet.wallets.invalidate();
			setShowConfetti(true);
		},
	});

	useEffect(() => {
		let timer: NodeJS.Timeout;
		if (showConfetti) {
			setTimeout(() => {
				setShowConfetti(false);
			}, 5000);
		}

		return () => {
			timer && clearTimeout(timer);
		};
	}, [showConfetti]);

	const hasWallets = wallets && wallets.length > 0;
	const shouldLoadingBtn = isPending || walletCreate.isPending;

	const renderCreateWalletScreen = () => {
		return (
			<>
				<Text fw="bold" my="xs">
					🚀 Welcome to your very own{" "}
					<Text fw="bolder" span variant="gradient">
						OpenAgent Wallet
					</Text>
					! 🌟
				</Text>

				<Text my="xs">
					OpenAgent Wallet is an{" "}
					<Text fw="bold" span>
						Account Abstraction (AA) Smart Contract Wallet
					</Text>{" "}
					that is a smarter, more secure, and more convenient way to interact
					with the blockchain. Together with OpenAgent&apos;s AI power, you can
					enjoy a seamless experience in the world of Web3.
				</Text>

				<Anchor
					c="dimmed"
					component={Link}
					href="/help/wallet"
					my="xs"
					size="xs"
					target="_blank"
				>
					Know more about the detail.
				</Anchor>

				{hasWallets && (
					<Text c="red">
						You already have a OpenAgent Wallet. So you can&apos;t create
						another for now.
					</Text>
				)}

				<Flex justify="flex-end">
					<Button
						disabled={hasWallets}
						loading={shouldLoadingBtn}
						onClick={() => {
							walletCreate.mutate();
						}}
					>
						✨ Create Wallet
					</Button>
				</Flex>
			</>
		);
	};

	const renderSuccessScreen = ({ close }: { close: () => void }) => {
		const wallet = wallets?.[0];
		return (
			<>
				<Text fw="bold" my="xs">
					🎉 Congratulations! 🎉
				</Text>

				<Text my="xs">
					You have successfully created your OpenAgent Wallet. You can now start
					interacting with the blockchain with AI power!
				</Text>

				{wallet && (
					<Text my="xs" size="xs">
						Address:{" "}
						<Text ff="monospace" fw="bold" span>
							{wallet.walletAddress}
						</Text>
					</Text>
				)}

				<Flex justify="flex-end">
					<Button
						onClick={() => {
							close();
						}}
					>
						👍 Got it!
					</Button>
				</Flex>
			</>
		);
	};

	return (
		<>
			<PageModal
				title={
					<>
						<IconWallet />
					</>
				}
				withCloseButton
			>
				{({ close }) => {
					if (walletCreate.isSuccess) {
						return renderSuccessScreen({ close });
					}

					return renderCreateWalletScreen();
				}}
			</PageModal>

			<Portal>
				<div className="fixed left-0 top-0 z-[50000]">
					<Confetti numberOfPieces={showConfetti ? 200 : 0} />
				</div>
			</Portal>
		</>
	);
}
