import { truncateAddress } from "@/lib/wagmi/utils";
import { Text, Tooltip } from "@mantine/core";

export function TxHash({ hash }: { hash: `0x${string}` }) {
	return (
		<Tooltip label={hash}>
			<Text ff="monospace">{truncateAddress(hash)}</Text>
		</Tooltip>
	);
}
