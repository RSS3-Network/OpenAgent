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

interface WalletSelectorProps extends InputBaseProps {
	onChange?: (value: number | undefined) => void;
	value?: number;
}

export function WalletSelectorWithSuspense({
	onChange,
	value,
	...props
}: WalletSelectorProps) {
	const [wallets] = api.wallet.wallets.useSuspenseQuery();

	const combobox = useCombobox();

	const Options = wallets.map((item) => (
		<ComboboxOption key={item.walletId} value={String(item.walletId)}>
			{truncateAddress(item.walletAddress)}
		</ComboboxOption>
	));

	const selectedWallet = wallets.find((item) => item.walletId === value);

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
					{selectedWallet?.walletAddress ? (
						truncateAddress(selectedWallet.walletAddress)
					) : (
						<InputPlaceholder>Pick a wallet</InputPlaceholder>
					)}
				</InputBase>
			</ComboboxTarget>

			<ComboboxDropdown>
				<ComboboxOptions>
					{Options.length === 0 ? (
						<ComboboxEmpty>
							<Button
								component={Link}
								href="/app/wallets/initialization"
								onClick={() => combobox.closeDropdown()}
								scroll={false}
								variant="subtle"
							>
								Create Wallet
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

export function WalletSelectorLoading({ label }: { label: React.ReactNode }) {
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

export function WalletSelector(props: WalletSelectorProps) {
	return (
		<Suspense fallback={<WalletSelectorLoading label={props.label} />}>
			<WalletSelectorWithSuspense {...props} />
		</Suspense>
	);
}
