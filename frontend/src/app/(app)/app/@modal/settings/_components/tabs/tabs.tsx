import { IconBrush, IconWallet } from "@tabler/icons-react";
import { ReactNode } from "react";

export const tabs = [
	{
		icon: <IconBrush size="1rem" stroke={1.5} />,
		id: "appearance",
		label: "Appearance",
	},
	{
		icon: <IconWallet size="1rem" stroke={1.5} />,
		id: "executors",
		label: "Executors",
	},
] as const satisfies ReadonlyArray<{
	icon: ReactNode;
	id: string;
	label: string;
}>;

export type TabId = (typeof tabs)[number]["id"];
