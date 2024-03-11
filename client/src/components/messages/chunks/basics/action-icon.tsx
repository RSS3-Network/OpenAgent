import { ActionIcon, CopyButton, Tooltip } from "@mantine/core";
import { IconCheck, IconCopy, IconExternalLink } from "@tabler/icons-react";
import Link from "next/link";

export function ActionIconCopy({ value }: { value: string }) {
	return (
		<CopyButton timeout={2000} value={value}>
			{({ copied, copy }) => (
				<Tooltip label={copied ? "Copied" : "Copy Address"} position="bottom">
					<ActionIcon
						color={copied ? "teal" : "gray"}
						onClick={copy}
						variant="subtle"
					>
						{copied ? <IconCheck size="1rem" /> : <IconCopy size="1rem" />}
					</ActionIcon>
				</Tooltip>
			)}
		</CopyButton>
	);
}

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
