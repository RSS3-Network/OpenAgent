"use client";

import {
	NavLink,
	Popover,
	PopoverDropdown,
	PopoverTarget,
	em,
} from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import { IconWallet } from "@tabler/icons-react";
import { useAtom } from "jotai/react";
import { atom } from "jotai/vanilla";

import { WalletsDropdown } from "./wallets-dropdown";

const walletDropdownOpenedAtom = atom(false);

export function useWalletDropdownOpened() {
	const [walletDropdownOpened, setWalletDropdownOpened] = useAtom(
		walletDropdownOpenedAtom
	);

	return {
		setWalletDropdownOpened,
		walletDropdownOpened,
	};
}

export function Wallets() {
	const { setWalletDropdownOpened, walletDropdownOpened } =
		useWalletDropdownOpened();

	const isMobile = useMediaQuery(`(max-width: ${em(750)})`);

	return (
		<Popover
			closeOnClickOutside
			offset={0}
			onClose={() => setWalletDropdownOpened(false)}
			opened={walletDropdownOpened}
			position={isMobile ? "bottom" : "right-start"}
			width={"target"}
		>
			<PopoverTarget>
				<NavLink
					active={walletDropdownOpened}
					label="Wallets"
					leftSection={<IconWallet size="1rem" stroke={1.5} />}
					onClick={() => setWalletDropdownOpened(!walletDropdownOpened)}
				/>
			</PopoverTarget>
			<PopoverDropdown>
				<WalletsDropdown />
			</PopoverDropdown>
		</Popover>
	);
}
