import { ActionIcon, CopyButton, Tooltip } from "@mantine/core";
import { IconCheck, IconCopy } from "@tabler/icons-react";

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
