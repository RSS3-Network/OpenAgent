/* eslint-disable perfectionist/sort-objects */
import type { Config } from "tailwindcss";

const config: Config = {
	content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
	darkMode: ["class", '[data-mantine-color-scheme="dark"]'],
	theme: {
		screens: {
			xs: "36em",
			sm: "40em",
			md: "48em",
			lg: "64em",
			xl: "80em",
			"2xl": "96em",
		},
		extend: {
			backgroundImage: {
				"gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
				"gradient-conic":
					"conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
			},
		},
	},
	plugins: [],
};
export default config;
