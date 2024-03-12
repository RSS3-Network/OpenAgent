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
	const { data: executors, isPending } = api.executor.executors.useQuery();
	const utils = api.useUtils();

	const [showConfetti, setShowConfetti] = useState(false);

	const executorCreate = api.executor.executorCreate.useMutation({
		async onSuccess() {
			await utils.executor.executors.invalidate();
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

	const hasExecutors = executors && executors.length > 0;
	const shouldLoadingBtn = isPending || executorCreate.isPending;

	const renderCreateExecutorScreen = () => {
		return (
			<>
				<Text fw="bold" my="xs">
					🚀 Welcome to your very own{" "}
					<Text fw="bolder" span variant="gradient">
						OpenAgent Executor
					</Text>
					! 🌟
				</Text>

				<Text my="xs">
					OpenAgent Executor is an{" "}
					<Text fw="bold" span>
						Account Abstraction (AA) Smart Contract Executor
					</Text>{" "}
					that is a smarter, more secure, and more convenient way to interact
					with the blockchain. Together with OpenAgent&apos;s AI power, you can
					enjoy a seamless experience in the world of Web3.
				</Text>

				<Anchor
					c="dimmed"
					component={Link}
					href="/help/executor"
					my="xs"
					size="xs"
					target="_blank"
				>
					Know more about the detail.
				</Anchor>

				{hasExecutors && (
					<Text c="red">
						You already have a OpenAgent Executor. So you can&apos;t create
						another for now.
					</Text>
				)}

				<Flex justify="flex-end">
					<Button
						disabled={hasExecutors}
						loading={shouldLoadingBtn}
						onClick={() => {
							executorCreate.mutate();
						}}
					>
						✨ Create Executor
					</Button>
				</Flex>
			</>
		);
	};

	const renderSuccessScreen = ({ close }: { close: () => void }) => {
		const executor = executors?.[0];
		return (
			<>
				<Text fw="bold" my="xs">
					🎉 Congratulations! 🎉
				</Text>

				<Text my="xs">
					You have successfully created your OpenAgent Executor. You can now
					start interacting with the blockchain with AI power!
				</Text>

				{executor && (
					<Text my="xs" size="xs">
						Address:{" "}
						<Text ff="monospace" fw="bold" span>
							{executor.executorAddress}
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
					if (executorCreate.isSuccess) {
						return renderSuccessScreen({ close });
					}

					return renderCreateExecutorScreen();
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
