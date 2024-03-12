import { Image } from "@mantine/core";

export function ExecutorAddressAvatar({
	size = 32,
	executorAddress,
}: {
	size?: number | string;
	executorAddress: `${string}.eth` | `0x${string}`;
}) {
	return (
		<Image
			alt="avatar"
			h={size}
			radius="xs"
			src={`https://cdn.stamp.fyi/avatar/${executorAddress}`}
			w={size}
		/>
	);
}
