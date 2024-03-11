"use client";

import { useAiNewSessionRouter } from "@/lib/ai/hooks";
import { Group, Kbd } from "@mantine/core";
import { useHotkeys } from "@mantine/hooks";
import {
	type SpotlightActionData,
	type SpotlightActionGroupData,
	spotlight,
} from "@mantine/spotlight";
import { IconPlus } from "@tabler/icons-react";

export function useActions() {
	const { pushNewSession } = useAiNewSessionRouter();
	useHotkeys(
		[
			["mod+j", () => console.log("Toggle color scheme")],
			["mod+k", () => spotlight.toggle()],
			["alt+c", () => pushNewSession()],
		],
		[] // tags to ignore
	);

	const actions: (SpotlightActionData | SpotlightActionGroupData)[] = [
		{
			actions: [
				{
					description: "Create new chat",
					id: "new-chat",
					label: "New chat",
					leftSection: <IconPlus />,
					onClick: () => pushNewSession(),
					rightSection: <HotKeyRenderer keys={["⌥", "C"]} />,
				},
			],
			group: "Chats",
		},
	];

	return {
		actions,
	};
}

function HotKeyRenderer({ keys }: { keys: string[] }) {
	return (
		<Group gap="xs">
			{keys.map((key, i) => (
				<Kbd key={i} size="md">
					{key}
				</Kbd>
			))}
		</Group>
	);
}
