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

import { ExecutorsDropdown } from "./executors-dropdown";

const executorDropdownOpenedAtom = atom(false);

export function useExecutorDropdownOpened() {
	const [executorDropdownOpened, setExecutorDropdownOpened] = useAtom(
		executorDropdownOpenedAtom
	);

	return {
		executorDropdownOpened,
		setExecutorDropdownOpened,
	};
}

export function Executors() {
	const { executorDropdownOpened, setExecutorDropdownOpened } =
		useExecutorDropdownOpened();

	const isMobile = useMediaQuery(`(max-width: ${em(750)})`);

	return (
		<Popover
			closeOnClickOutside
			offset={0}
			onClose={() => setExecutorDropdownOpened(false)}
			opened={executorDropdownOpened}
			position={isMobile ? "bottom" : "right-start"}
			width={"target"}
		>
			<PopoverTarget>
				<NavLink
					active={executorDropdownOpened}
					label="Executors"
					leftSection={<IconWallet size="1rem" stroke={1.5} />}
					onClick={() => setExecutorDropdownOpened(!executorDropdownOpened)}
				/>
			</PopoverTarget>
			<PopoverDropdown>
				<ExecutorsDropdown />
			</PopoverDropdown>
		</Popover>
	);
}
