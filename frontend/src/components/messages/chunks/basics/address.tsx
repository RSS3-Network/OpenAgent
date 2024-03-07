import { truncateAddress } from "@/lib/wagmi/utils";
import { Text, type TextProps, Tooltip } from "@mantine/core";

export function Address({
	address,
	...props
}: { address: `0x${string}` } & TextProps) {
	return (
		<Tooltip label={address} position="bottom">
			<Text ff="monospace" {...props}>
				{truncateAddress(address)}
			</Text>
		</Tooltip>
	);
}
