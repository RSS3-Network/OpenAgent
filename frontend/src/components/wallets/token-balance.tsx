import { Group, Image, NumberFormatter, rem } from "@mantine/core";
import { formatUnits } from "viem";

export function TokenBalance({
	address,
	balance,
	decimals,
	imgUrl,
	name,
	symbol,
}: {
	address: `0x${string}`;
	/** in wei */
	balance: string;
	decimals: number;
	imgUrl: string;
	name: string;
	symbol: string;
}) {
	return (
		<Group gap="xs">
			<Image alt={name} h={rem(20)} src={imgUrl} w={rem(20)} />

			<NumberFormatter
				suffix={" " + symbol}
				value={formatUnits(BigInt(balance), decimals)}
			/>
		</Group>
	);
}
