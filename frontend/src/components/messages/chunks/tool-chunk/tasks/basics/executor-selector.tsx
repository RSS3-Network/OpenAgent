"use client";

import { api } from "@/lib/trpc/client";
import { truncateAddress } from "@/lib/wagmi/utils";
import {
	Button,
	Combobox,
	ComboboxDropdown,
	ComboboxEmpty,
	ComboboxOption,
	ComboboxOptions,
	ComboboxTarget,
	InputBase,
	InputBaseProps,
	InputPlaceholder,
	useCombobox,
} from "@mantine/core";
import Link from "next/link";
import { Suspense, useState } from "react";

interface ExecutorSelectorProps extends InputBaseProps {
	onChange?: (value: number | undefined) => void;
	value?: number;
}

export function ExecutorSelectorWithSuspense({
	onChange,
	value,
	...props
}: ExecutorSelectorProps) {
	const [executors] = api.executor.executors.useSuspenseQuery();

	const combobox = useCombobox();

	const Options = executors.map((item) => (
		<ComboboxOption key={item.executorId} value={String(item.executorId)}>
			{truncateAddress(item.executorAddress)}
		</ComboboxOption>
	));

	const selectedExecutor = executors.find((item) => item.executorId === value);

	return (
		<Combobox
			onOptionSubmit={(optionValue) => {
				onChange?.(parseInt(optionValue, 10));
				combobox.closeDropdown();
			}}
			store={combobox}
		>
			<ComboboxTarget>
				<InputBase
					component="button"
					onClick={() => combobox.toggleDropdown()}
					pointer
					rightSection={<Combobox.Chevron />}
					rightSectionPointerEvents="none"
					type="button"
					{...props}
				>
					{selectedExecutor?.executorAddress ? (
						truncateAddress(selectedExecutor.executorAddress)
					) : (
						<InputPlaceholder>Pick a executor</InputPlaceholder>
					)}
				</InputBase>
			</ComboboxTarget>

			<ComboboxDropdown>
				<ComboboxOptions>
					{Options.length === 0 ? (
						<ComboboxEmpty>
							<Button
								component={Link}
								href="/app/executors/initialization"
								onClick={() => combobox.closeDropdown()}
								scroll={false}
								variant="subtle"
							>
								Create Executor
							</Button>
						</ComboboxEmpty>
					) : (
						Options
					)}
				</ComboboxOptions>
			</ComboboxDropdown>
		</Combobox>
	);
}

export function ExecutorSelectorLoading({ label }: { label: React.ReactNode }) {
	return (
		<InputBase
			component="button"
			disabled
			label={label}
			pointer
			rightSection={<Combobox.Chevron />}
			rightSectionPointerEvents="none"
			type="button"
		>
			Loading...
		</InputBase>
	);
}

export function ExecutorSelector(props: ExecutorSelectorProps) {
	return (
		<Suspense fallback={<ExecutorSelectorLoading label={props.label} />}>
			<ExecutorSelectorWithSuspense {...props} />
		</Suspense>
	);
}
