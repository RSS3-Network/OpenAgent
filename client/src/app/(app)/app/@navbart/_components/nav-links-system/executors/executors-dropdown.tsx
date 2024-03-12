"use client";

import { api } from "@/lib/trpc/client";
import { Button, Skeleton, Stack, Text } from "@mantine/core";
import Link from "next/link";
import { Suspense } from "react";

import { useExecutorDropdownOpened } from ".";
import { ExecutorDetail } from "./executor-detail";

function ExecutorsDropdownWithSuspense() {
	const [executors] = api.executor.executors.useSuspenseQuery();

	const { setExecutorDropdownOpened } = useExecutorDropdownOpened();

	if (executors.length === 0) {
		return (
			<Stack align="center">
				<Text c="dimmed" size="xs">
					No executors yet.
				</Text>

				<Button
					component={Link}
					href="/app/executors/initialization"
					onClick={() => setExecutorDropdownOpened(false)}
					scroll={false}
				>
					Create Executor
				</Button>
			</Stack>
		);
	}

	return <ExecutorDetail executorId={executors[0].executorId} />;
}

function ExecutorDropdownSkeleton() {
	return <Skeleton h={50} />;
}

export function ExecutorsDropdown() {
	return (
		<Suspense fallback={<ExecutorDropdownSkeleton />}>
			<ExecutorsDropdownWithSuspense />
		</Suspense>
	);
}
