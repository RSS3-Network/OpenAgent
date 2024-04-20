"use client";

import { ActionIconCopy } from "@/components/action-icons/copy";
import { ActionIconExternalLink } from "@/components/action-icons/external-link";
import { ExecutorAddressAvatar } from "@/components/executor/executor-address-avatar";
import { ExecutorAddressDisplay } from "@/components/executor/executor-address-display";
import { TokenBalance } from "@/components/executor/token-balance";
import { api } from "@/lib/trpc/client";
import { Group, Skeleton, Stack, Text, rem } from "@mantine/core";
import { Suspense } from "react";

function ExecutorDetailWithSuspense({ executorId }: { executorId: number }) {
	const [executor] = api.executor.executor.useSuspenseQuery({ executorId });

	if (!executor) {
		return <>NOT FOUND</>;
	}

	return (
		<Stack>
			<div>
				<Text fw="bold">Address</Text>
				<Group gap="xs">
					<ExecutorAddressAvatar
						executorAddress={executor.executorAddress}
						size={rem(16)}
					/>
					<ExecutorAddressDisplay executorAddress={executor.executorAddress} />
					<ActionIconCopy value={executor.executorAddress} />
					<ActionIconExternalLink
						href={`https://hoot.it/${executor.executorAddress}`}
						label="View on Hoot.it"
					/>
				</Group>
			</div>

			<div>
				<Text fw="bold">Balance</Text>
				{executor.balance.map((token) => (
					<TokenBalance
						balance={token.tokenBalance}
						decimals={token.tokenDecimal}
						executorAddress={executor.executorAddress}
						imgUrl={token.tokenImageUrl}
						key={token.tokenAddress}
						name={token.tokenName}
						symbol={token.tokenSymbol}
						tokenAddress={token.tokenAddress}
					/>
				))}
			</div>
		</Stack>
	);
}
function ExecutorDetailSkeleton() {
	return <Skeleton h={50} />;
}

export function ExecutorDetail({ executorId }: { executorId: number }) {
	return (
		<Suspense fallback={<ExecutorDetailSkeleton />}>
			<ExecutorDetailWithSuspense executorId={executorId} />
		</Suspense>
	);
}
