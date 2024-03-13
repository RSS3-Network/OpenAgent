"use client";

import {
	ActionIcon,
	useComputedColorScheme,
	useMantineColorScheme,
} from "@mantine/core";
import { IconMoon, IconSun } from "@tabler/icons-react";

export function ColorSchemeSwitch() {
	const { setColorScheme } = useMantineColorScheme();
	const computedColorScheme = useComputedColorScheme("light", {
		getInitialValueInEffect: true,
	});

	return (
		<ActionIcon
			aria-label="Toggle color scheme"
			onClick={() =>
				setColorScheme(computedColorScheme === "light" ? "dark" : "light")
			}
			size="xs"
			variant="default"
		>
			<IconSun className="block dark:hidden" stroke={1.5} />
			<IconMoon className="hidden dark:block" stroke={1.5} />
		</ActionIcon>
	);
}

export function ColorSchemeSwitchIndicator() {
	if (process.env.NODE_ENV === "production") return null;

	return (
		<div className="fixed bottom-1 right-1 z-[9999] font-mono text-xs">
			<ColorSchemeSwitch />
		</div>
	);
}
