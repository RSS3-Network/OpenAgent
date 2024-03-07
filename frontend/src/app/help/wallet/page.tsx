import { TypographyStylesProvider } from "@mantine/core";

export default function Page() {
	return (
		<TypographyStylesProvider>
			<div
				dangerouslySetInnerHTML={{
					__html: `
					<h1>OpenAgent Wallet</h1>
					<h2>What is OpenAgent Wallet?</h2>
`,
				}}
			></div>
		</TypographyStylesProvider>
	);
}
