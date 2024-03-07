"use client";

import { DEFAULT_THEME, createTheme, mergeMantineTheme } from "@mantine/core";

const themeOverride = createTheme({
	components: {
		Modal: {
			defaultProps: {
				overlayProps: {
					backgroundOpacity: 0.3,
					blur: 1,
				},
			},
		},
		Tooltip: {
			styles: {
				tooltip: {
					background: "var(--mantine-color-default)",
					boxShadow: "var(--mantine-shadow-sm)",
					color: "var(--mantine-color-text)",
				},
			},
		},
		TooltipFloating: {
			styles: {
				tooltip: {
					background: "var(--mantine-color-default)",
					boxShadow: "var(--mantine-shadow-sm)",
					color: "var(--mantine-color-text)",
				},
			},
		},
	},
	primaryColor: "blue",
});

export const theme = mergeMantineTheme(DEFAULT_THEME, themeOverride);
