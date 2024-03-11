import { Image } from "@mantine/core";

export function WalletAddressAvatar({
	size = 32,
	walletAddress,
}: {
	size?: number | string;
	walletAddress: `${string}.eth` | `0x${string}`;
}) {
	return (
		<Image
			alt="avatar"
			h={size}
			radius="xs"
			src={`https://cdn.stamp.fyi/avatar/${walletAddress}`}
			w={size}
		/>
	);
}
