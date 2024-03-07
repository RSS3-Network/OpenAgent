import { ActionIcon, Tooltip } from "@mantine/core";
import { IconExternalLink } from "@tabler/icons-react";
import Link from "next/link";

export function ActionIconExternalLink({
	href,
	label,
}: {
	href: string;
	label: string;
}) {
	return (
		<Tooltip label={label} position="bottom">
			<ActionIcon
				color="gray"
				component={Link}
				href={href}
				target="_blank"
				variant="subtle"
			>
				<IconExternalLink size="1rem" />
			</ActionIcon>
		</Tooltip>
	);
}
