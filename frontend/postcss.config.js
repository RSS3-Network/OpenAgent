module.exports = {
	plugins: {
		"tailwindcss/nesting": {},
		tailwindcss: {},
		autoprefixer: {},
		"postcss-preset-mantine": {},
		"postcss-simple-vars": {
			variables: {
				"mantine-breakpoint-xs": "36em",
				"mantine-breakpoint-sm": "40em",
				"mantine-breakpoint-md": "48em",
				"mantine-breakpoint-lg": "64em",
				"mantine-breakpoint-xl": "80em",
				"mantine-breakpoint-2xl": "96em",
			},
		},
	},
};
