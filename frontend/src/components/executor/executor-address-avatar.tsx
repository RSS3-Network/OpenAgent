import { Image } from "@mantine/core";

export function ExecutorAddressAvatar({
	executorAddress,
	size = 32,
}: {
	executorAddress: `${string}.eth` | `0x${string}`;
	size?: number | string;
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
