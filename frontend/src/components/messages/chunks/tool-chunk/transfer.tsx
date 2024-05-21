import { ethAddress } from "@/lib/validations/pipelines/eth-address";
import { ethName } from "@/lib/validations/pipelines/eth-name";
import { valibotResolver } from "@/lib/validations/resolver";
import { AiSessionMessageToolOutputBody_Transfer } from "@/server/api/routers/ai/types/session";
import {
	Alert,
	Button,
	Card,
	Group,
	Image,
	LoadingOverlay,
	Text,
	TextInput,
	rem,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { showNotification } from "@mantine/notifications";
import { useConnectModal } from "@rainbow-me/rainbowkit";
import { IconCircleCheck, IconInfoCircle } from "@tabler/icons-react";
import { m } from "framer-motion";
import { Suspense, useMemo, useState } from "react";
import { type Input, object, string, union } from "valibot";
import { Address, parseEther } from "viem";
import {
	useAccount,
	useChains,
	useSendTransaction,
	useSwitchChain,
	useWaitForTransactionReceipt,
} from "wagmi";

import { TaskLoading } from "./task-loading";

const schema = object({
	amount: string(),
	toAddress: union(
		[string([ethAddress()]), string([ethName()])],
		"Must be a valid Ethereum address or ENS name."
	),
});

type FormData = Input<typeof schema>;

function ToolChunkTransferWithSuspense({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Transfer;
}) {
	const switchChain = useSwitchChain();
	const transfer = useSendTransaction({
		mutation: {
			onError: (error) => {
				showNotification({
					color: "red",
					message: error.message,
					title: "Transfer failed",
				});
			},
		},
	});
	const account = useAccount();
	const { openConnectModal } = useConnectModal();
	const [isCanceled, setCanceled] = useState(false);
	const { isLoading: isConfirming, isSuccess: isConfirmed } =
		useWaitForTransactionReceipt({ hash: transfer.data });

	const form = useForm<FormData>({
		initialValues: {
			amount: body.amount,
			toAddress: body.to_address,
		},
		validate: valibotResolver(schema),
	});

	const disableForm =
		transfer.isPending || isConfirming || isCanceled || isConfirmed;

	return (
		<>
			<LoadingOverlay
				loaderProps={{ children: "CANCELED" }}
				visible={isCanceled}
				zIndex={1}
			/>
			<form
				className="mt-2 space-y-2"
				onSubmit={form.onSubmit((values) => {
					transfer.sendTransaction({
						chainId: Number(body.chain_id),
						to: values.toAddress as Address,
						value: parseEther(values.amount),
					});
				})}
			>
				<TextInput
					disabled
					label="From:"
					placeholder="Please connect wallet"
					readOnly
					value={account.address}
				/>

				<TextInput
					label="To:"
					placeholder="0x..."
					withAsterisk
					{...form.getInputProps("toAddress")}
					disabled={disableForm}
				/>

				<TextInput
					label="Amount:"
					placeholder="0.00"
					withAsterisk
					{...form.getInputProps("amount")}
					disabled={disableForm}
				/>

				<Group justify="flex-end" mt="md">
					{isConfirmed ? (
						<Alert
							className="w-full"
							color="green"
							icon={<IconCircleCheck />}
							variant="light"
						>
							Transaction confirmed.
						</Alert>
					) : (
						<>
							<Button
								color="red"
								disabled={disableForm}
								onClick={() => setCanceled(true)}
								type="button"
								variant="light"
							>
								Cancel
							</Button>

							{account.status === "connected" ? (
								account.chainId === Number(body.chain_id) ? (
									<Button disabled={disableForm} type="submit">
										Transfer
									</Button>
								) : (
									<Button
										disabled={disableForm}
										onClick={() => {
											switchChain.switchChain({
												chainId: Number(body.chain_id),
											});
										}}
										type="button"
									>
										Switch Network
									</Button>
								)
							) : (
								<Button
									disabled={disableForm}
									onClick={() => openConnectModal?.()}
									type="button"
								>
									Connect Wallet
								</Button>
							)}
						</>
					)}
				</Group>
			</form>
		</>
	);
}

export function ToolChunkTransfer(props: {
	body: AiSessionMessageToolOutputBody_Transfer;
	expired: boolean;
}) {
	const chains = useChains();
	const chain = useMemo(
		() => chains.find((chain) => chain.id === Number(props.body.chain_id)),
		[chains, props.body.chain_id]
	);

	if (props.expired) {
		return (
			<div className="flex items-center gap-2 rounded-sm bg-gray-300 px-4 py-2">
				<IconInfoCircle className="size-5" />
				The transfer has expired.
			</div>
		);
	}

	if (!chain) {
		return (
			<div className="flex items-center gap-2 rounded-sm bg-red-200 px-4 py-2">
				<IconInfoCircle className="size-5" />
				Unsupported chain ID: {props.body.chain_id}
			</div>
		);
	}

	return (
		<Suspense fallback={<TaskLoading taskId="ToolChunkTransfer" />}>
			<Card component={m.div} layoutId="ToolChunkTransfer" w={300}>
				<Group gap="xs">
					{props.body.logoURI && (
						<Image
							alt="Token Logo"
							h={rem(16)}
							src={props.body.logoURI}
							w={rem(16)}
						/>
					)}
					<Text fw="bold">
						Transfer {props.body.token} on {chain.name}
					</Text>
				</Group>

				<ToolChunkTransferWithSuspense {...props} />
			</Card>
		</Suspense>
	);
}
