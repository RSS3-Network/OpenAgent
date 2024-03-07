"use client";

import { Select, Title, useMantineColorScheme } from "@mantine/core";

export default function AppearanceSection() {
	const { colorScheme, setColorScheme } = useMantineColorScheme();

	return (
		<div>
			<Title order={4}>Appearance</Title>

			<Select
				checkIconPosition="right"
				data={[
					{
						label: "Auto",
						value: "auto",
					},
					{
						label: "Light",
						value: "light",
					},
					{
						label: "Dark",
						value: "dark",
					},
				]}
				label="Color scheme"
				onChange={(e) => setColorScheme(e?.toLowerCase() as any)}
				value={colorScheme}
			/>
		</div>
	);
}
