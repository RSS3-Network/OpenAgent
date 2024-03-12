import { api } from "@/lib/trpc/client";
import { truncateAddress } from "@/lib/wagmi/utils";
import { Text, Tooltip } from "@mantine/core";
import { Suspense } from "react";

function ExecutorAddressFromIdDisplayWithSuspense({
	executorId,
}: {
	executorId: number;
}) {
	const [executor] = api.executor.executor.useSuspenseQuery({ executorId });
	return (
		<Tooltip label={executor.executorAddress}>
			<Text ff="monospace">{truncateAddress(executor.executorAddress)}</Text>
		</Tooltip>
	);
}

export function ExecutorAddressFromIdDisplay({
	executorId,
}: {
	executorId: number;
}) {
	return (
		<Suspense fallback={<div>0x...</div>}>
			{executorId > 0 ? (
				<ExecutorAddressFromIdDisplayWithSuspense executorId={executorId} />
			) : (
				<Text ff="monospace">UNKNOWN</Text>
			)}
		</Suspense>
	);
}

export function ExecutorAddressDisplay({
	executorAddress,
}: {
	executorAddress: `${string}.eth` | `0x${string}`;
}) {
	return (
		<Tooltip label={executorAddress}>
			<Text ff="monospace">{truncateAddress(executorAddress)}</Text>
		</Tooltip>
	);
}
