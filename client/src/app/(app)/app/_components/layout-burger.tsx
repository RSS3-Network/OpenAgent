"use client";

import { Burger, Tooltip } from "@mantine/core";
import { atom, useAtom } from "jotai";

const atomBurgerOpenDesktop = atom<boolean>(true);
const atomBurgerOpenMobile = atom<boolean>(false);

export function useBurgerOpen() {
	const desktop = useAtom(atomBurgerOpenDesktop);
	const mobile = useAtom(atomBurgerOpenMobile);
	return {
		desktop,
		mobile,
	};
}

export function LayoutBurger() {
	const { desktop, mobile } = useBurgerOpen();

	return (
		<>
			{/* mobile */}
			<Tooltip
				label={mobile[0] ? "Close Navbar" : "Open Navbar"}
				openDelay={500}
			>
				<Burger
					aria-label="Toggle navigation"
					hiddenFrom="sm"
					onClick={(e) => {
						e.stopPropagation();
						mobile[1]((o) => !o);
					}}
					opened={mobile[0]}
					size="sm"
				/>
			</Tooltip>

			{/* desktop */}
			<Tooltip
				label={desktop[0] ? "Close Navbar" : "Open Navbar"}
				openDelay={500}
			>
				<Burger
					aria-label="Toggle navigation"
					hidden={desktop[0]}
					onClick={(e) => {
						e.stopPropagation();
						desktop[1]((o) => !o);
					}}
					opened={desktop[0]}
					size="sm"
					visibleFrom="sm"
				/>
			</Tooltip>
		</>
	);
}
