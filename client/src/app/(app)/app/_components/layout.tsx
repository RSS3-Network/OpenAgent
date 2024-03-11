"use client";

import { AppShell, Group } from "@mantine/core";
import { type ReactNode } from "react";

import { LayoutBurger, useBurgerOpen } from "./layout-burger";
import { LayoutNavbar, useNavbarWidth } from "./layout-navbar";

export function AppLayout({
	children,
	headerl,
	headerr,
	modal,
	navbard,
	navbart,
}: {
	children: ReactNode;
	headerl: ReactNode;
	headerr: ReactNode;
	modal: ReactNode;
	navbard: ReactNode;
	navbart: ReactNode;
}) {
	const { desktop, mobile } = useBurgerOpen();

	const navbarWidth = useNavbarWidth();

	return (
		<AppShell
			footer={{ height: 60 }}
			header={{ height: 60 }}
			layout="alt"
			navbar={{
				breakpoint: "sm",
				collapsed: {
					desktop: !desktop[0],
					mobile: !mobile[0],
				},
				width: navbarWidth,
			}}
			// aside={{
			// 	width: 300,
			// 	breakpoint: "md",
			// 	collapsed: { desktop: false, mobile: true },
			// }}
			// padding="md"
			pr="0"
		>
			<AppShell.Header>
				<Group h="100%" justify="space-between">
					<Group h="100%" px="md">
						<LayoutBurger />
						{headerl}
					</Group>

					<Group h="100%" px="md">
						{headerr}
					</Group>
				</Group>
			</AppShell.Header>

			<LayoutNavbar>
				<AppShell.Section>{navbart}</AppShell.Section>

				{navbard}
			</LayoutNavbar>

			<AppShell.Main
			//maw={rem(1000)}
			//mx="auto"
			>
				{children}
			</AppShell.Main>

			{modal}
		</AppShell>
	);
}
