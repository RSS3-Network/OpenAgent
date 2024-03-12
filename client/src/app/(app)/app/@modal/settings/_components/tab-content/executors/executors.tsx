"use client";

import { api } from "@/lib/trpc/client";
import { Accordion, Alert, Button, Image, Text, Title } from "@mantine/core";
import { Suspense } from "react";

export function Executors_() {
	const [executors] = api.executor.executors.useSuspenseQuery();

	const utils = api.useUtils();
	const executorCreate = api.executor.executorCreate.useMutation({
		onSuccess: () => {
			utils.executor.executors.invalidate();
		},
	});

	if (executors.length === 0) {
		return (
			<Alert title="No Executors" variant="light" w="100%">
				<Text>
					You can still use OpenAgent without a executor, but you won&apos;t be
					able to interact with the blockchain.
				</Text>
				<Text>Click the button below to create a executor instantly.</Text>
				<Button
					loading={executorCreate.isPending}
					my="md"
					onClick={() => {
						executorCreate.mutate();
					}}
				>
					✨ Create Executor
				</Button>
			</Alert>
		);
	}

	return (
		<Accordion variant="separated">
			{executors.map((executor) => (
				<Accordion.Item
					key={executor.executorId}
					value={executor.executorAddress}
				>
					<Accordion.Control
						icon={
							<Image
								alt="Executor"
								height="16px"
								src={`https://cdn.stamp.fyi/avatar/${executor.executorAddress}`}
								width="16px"
							/>
						}
					>
						{executor.executorAddress}
					</Accordion.Control>
					<Accordion.Panel>{executor.executorAddress}</Accordion.Panel>
				</Accordion.Item>
			))}
		</Accordion>
	);
}

export function Executors() {
	return (
		<>
			<Title order={4} w="100%">
				Executors
			</Title>
			<Suspense fallback={<>loading...</>}>
				<Executors_ />
			</Suspense>
		</>
	);
}
