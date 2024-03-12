import { currentIdleTaskAtom } from "@/lib/ai/stores";
import { api } from "@/lib/trpc/client";
import { ethAddress } from "@/lib/validations/pipelines/eth-address";
import { ethName } from "@/lib/validations/pipelines/eth-name";
import { valibotResolver } from "@/lib/validations/resolver";
import { truncateAddress } from "@/lib/wagmi/utils";
import {
	Button,
	Card,
	Group,
	Image,
	Loader,
	LoadingOverlay,
	Text,
	TextInput,
	rem,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { showNotification } from "@mantine/notifications";
import { IconCircleCheck, IconCircleX } from "@tabler/icons-react";
import { m } from "framer-motion";
import { useSetAtom } from "jotai";
import { Suspense, useEffect } from "react";
import { type Input, number, object, string, union } from "valibot";

import { TaskLoading } from "./basics/task-loading";
import { ExecutorSelector } from "./basics/executor-selector";

const schema = object({
	amount: string(),
	toAddress: union(
		[string([ethAddress()]), string([ethName()])],
		"Must be a valid Ethereum address or ENS name."
	),
	executorId: number(),
});

type FormData = Input<typeof schema>;

function ToolChunkTransferWithSuspense({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Transfer;
}) {
	const [task] = api.ai.tasks.detail.useSuspenseQuery(
		{ taskId: body.task_id },
		{
			refetchInterval: (query) => {
				return query.state.data?.status === "pending" ||
					query.state.data?.status === "running"
					? 1000
					: false;
			},
		}
	);
	const [executors] = api.executor.executors.useSuspenseQuery();
	const setCurrentIdleTask = useSetAtom(currentIdleTaskAtom);

	useEffect(() => {
		if (task?.status === "idle") {
			setCurrentIdleTask(task);
		} else {
			setCurrentIdleTask(undefined);
		}

		return () => {
			setCurrentIdleTask(undefined);
		};
	}, [setCurrentIdleTask, task]);

	const form = useForm<FormData>({
		initialValues: {
			amount: body.amount,
			toAddress: body.to_address,
			executorId:
				executors && executors.length > 0 ? executors[0].executorId : 0,
		},
		validate: valibotResolver(schema),
	});

	useEffect(() => {
		if (executors && executors.length > 0 && form.values.executorId === 0) {
			form.setFieldValue("executorId", executors[0].executorId);
			form.resetDirty();
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [executors]);

	const utils = api.useUtils();

	const cancel = api.ai.tasks.cancel.useMutation({
		onError(err, newData, ctx: any) {
			// If the mutation fails, use the context-value from onMutate
			showNotification({
				color: "red",
				message: err.message ?? "Please try again later.",
				title: "Failed to cancel task",
			});

			utils.ai.tasks.detail.setData({ taskId: body.task_id }, ctx.prevData);
		},
		async onMutate() {
			// cancel outgoing request
			await utils.ai.tasks.detail.cancel({ taskId: body.task_id });
			// Get the data from the queryCache
			const prevData = utils.ai.tasks.detail.getData();
			// Optimistically update the task status to "canceled" to prevent
			utils.ai.tasks.detail.setData({ taskId: body.task_id }, (old) => ({
				...old!,
				status: "canceled",
			}));
			return { prevData };
		},
		async onSettled() {
			// Sync with server once mutation has settled
			await utils.ai.tasks.detail.invalidate({ taskId: body.task_id });
		},
	});

	const transfer = api.ai.tasks.actions.transfer.useMutation({
		onError(error, variables, context) {
			showNotification({
				color: "red",
				message: error.message ?? "Please try again later.",
				title: "Failed to transfer",
			});
		},
		async onSuccess() {
			await utils.ai.tasks.detail.invalidate({ taskId: body.task_id });
		},
	});

	if (!task) {
		return "Task not found";
	}

	if (
		task.status === "running" ||
		task.status === "done" ||
		task.status === "failed"
	) {
		const fromExecutor = executors.find(
			(executor) => executor.executorId === task.body.executor_id
		);

		return (
			<>
				<Text fw="bold">From</Text>
				<Text>
					{fromExecutor?.executorAddress &&
						truncateAddress(fromExecutor?.executorAddress)}
				</Text>

				<Text fw="bold">To</Text>
				<Text>{truncateAddress(task.body.to_address)}</Text>

				<Text fw="bold">Amount</Text>
				<Text>{task.body.amount}</Text>

				<Text fw="bold">Status</Text>

				<Group gap="xs">
					{task.status === "running" && (
						<>
							<Loader size="1rem" type="oval" />
							<Text c="dimmed" span>
								Running
							</Text>
						</>
					)}
					{task.status === "done" && (
						<>
							<IconCircleCheck color="var(--mantine-color-green-filled)" />
							<Text c="green" span>
								Done
							</Text>
						</>
					)}
					{task.status === "failed" && (
						<>
							<IconCircleX color="var(--mantine-color-red-filled)" />
							<Text c="red" span>
								Failed
							</Text>
						</>
					)}
				</Group>
			</>
		);
	}

	return (
		<>
			<LoadingOverlay
				loaderProps={{ children: "CANCELED" }}
				visible={task?.status === "canceled"}
				zIndex={1}
			/>
			<form
				onSubmit={form.onSubmit((values) => {
					console.log({ values });
					transfer.mutate({
						amount: values.amount,
						taskId: body.task_id,
						toAddress: values.toAddress,
						tokenAddress: body.token_address,
						executorId: values.executorId,
					});
				})}
			>
				<ExecutorSelector
					label="From"
					withAsterisk
					{...form.getInputProps("executorId")}
					disabled={transfer.isPending}
				/>

				<TextInput
					label="To"
					placeholder="0x..."
					withAsterisk
					{...form.getInputProps("toAddress")}
					disabled={transfer.isPending}
				/>

				<TextInput
					label="Amount"
					placeholder="0.00"
					withAsterisk
					{...form.getInputProps("amount")}
					disabled={transfer.isPending}
				/>

				<Group justify="flex-end" mt="md">
					<Button
						color="red"
						disabled={transfer.isPending}
						onClick={(e) => {
							e.preventDefault();
							cancel.mutate({ taskId: body.task_id });
						}}
						type="submit"
						variant="light"
					>
						Cancel
					</Button>
					<Button loading={transfer.isPending} type="submit">
						Transfer
					</Button>
				</Group>
			</form>
		</>
	);
}

export function ToolChunkTransfer(props: {
	body: AiSessionMessageToolOutputBody_Transfer;
}) {
	return (
		<Suspense fallback={<TaskLoading taskId={props.body.task_id} />}>
			<Card component={m.div} layoutId={props.body.task_id} w={300}>
				<Group gap="xs">
					<Image
						alt="Token Logo"
						h={rem(16)}
						src={props.body.logoURI}
						w={rem(16)}
					/>
					<Text fw="bold">Transfer {props.body.token}</Text>
				</Group>

				<ToolChunkTransferWithSuspense {...props} />
			</Card>
		</Suspense>
	);
}
