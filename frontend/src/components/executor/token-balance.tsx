import { chainId } from "@/lib/wagmi/config";
import {
	Button,
	Group,
	Image,
	NumberFormatter,
	NumberInput,
	rem,
} from "@mantine/core";
import { closeAllModals, openModal } from "@mantine/modals";
import { showNotification } from "@mantine/notifications";
import { useConnectModal } from "@rainbow-me/rainbowkit";
import { erc20Abi, formatUnits, parseEther, parseUnits } from "viem";
import {
	type BaseError,
	useAccount,
	useSendTransaction,
	useSwitchChain,
	useWaitForTransactionReceipt,
	useWriteContract,
} from "wagmi";

export function TokenBalance({
	balance,
	decimals,
	executorAddress,
	imgUrl,
	name,
	symbol,
	tokenAddress,
}: {
	/** in wei */
	balance: string;
	decimals: number;
	executorAddress: `0x${string}`;
	imgUrl: string;
	name: string;
	symbol: string;
	tokenAddress: `0x${string}`;
}) {
	// check connect
	const { chainId: currentChainId, isConnected } = useAccount();
	const { switchChain } = useSwitchChain();
	const { openConnectModal } = useConnectModal();

	const handleDeposit = () => {
		if (!isConnected) {
			openConnectModal?.();
			return;
		}

		if (currentChainId !== chainId) {
			switchChain({ chainId });
			return;
		}

		openModal({
			centered: true,
			children: (
				<DepositModal
					decimals={decimals}
					executorAddress={executorAddress}
					symbol={symbol}
					tokenAddress={tokenAddress}
				/>
			),
			closeOnClickOutside: false,
			id: "deposit",
			title: `Deposit $${symbol}`,
		});
	};

	return (
		<Group gap="xs">
			<Image alt={name} h={rem(20)} src={imgUrl} w={rem(20)} />

			<NumberFormatter
				suffix={" " + symbol}
				value={formatUnits(BigInt(balance), decimals)}
			/>

			<Button onClick={handleDeposit} size="compact-sm">
				Deposit
			</Button>
		</Group>
	);
}

function DepositModal({
	decimals,
	executorAddress,
	symbol,
	tokenAddress,
}: {
	decimals: number;
	executorAddress: `0x${string}`;
	symbol: string;
	tokenAddress: `0x${string}`;
}) {
	// deposit
	const isErc20 = tokenAddress !== "0x0000000000000000000000000000000000000000";

	const {
		data: hash1,
		error: error1,
		isPending: isPending1,
		sendTransaction,
	} = useSendTransaction();

	const {
		data: hash2,
		error: error2,
		isPending: isPending2,
		writeContract,
	} = useWriteContract();

	const hash = isErc20 ? hash2 : hash1;
	const error = isErc20 ? error2 : error1;
	const isPending = isErc20 ? isPending2 : isPending1;

	const { isLoading: isConfirming, isSuccess: isConfirmed } =
		useWaitForTransactionReceipt({
			hash,
		});

	const submit = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		const formData = new FormData(e.target as HTMLFormElement);
		const value = formData.get("value") as string;
		if (!value) return;
		if (isErc20) {
			writeContract(
				{
					abi: erc20Abi,
					address: tokenAddress,
					args: [executorAddress, parseEther(value)],
					chainId,
					functionName: "transfer",
				},
				{
					onError: (error) => {
						console.log(error, 111);
						showNotification({
							color: "red",
							message: error.message,
						});
					},
				}
			);
		} else {
			sendTransaction(
				{
					chainId,
					to: executorAddress,
					value: parseUnits(value, decimals),
				},
				{
					onError: (error) => {
						showNotification({
							color: "red",
							message: error.message,
						});
					},
				}
			);
		}
	};

	return (
		<form onSubmit={submit}>
			<NumberInput
				disabled={isPending}
				label="Amount"
				my="md"
				name="value"
				placeholder="0.00"
				required
				withAsterisk
			/>
			{hash && <div>Transaction Hash: {hash}</div>}
			{isConfirming && <div>Waiting for confirmation...</div>}
			{isConfirmed && <div>Transaction confirmed.</div>}
			{error && (
				<div>Error: {(error as BaseError).shortMessage || error.message}</div>
			)}

			{!isConfirmed ? (
				<Button loading={isPending || isConfirming} type="submit">
					Deposit
				</Button>
			) : (
				<Button onClick={() => closeAllModals()}>Done</Button>
			)}
		</form>
	);
}
