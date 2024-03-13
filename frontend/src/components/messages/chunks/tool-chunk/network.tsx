import { Card, Group, Text } from "@mantine/core";

import { Counter } from "../basics/counter";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkNetwork({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Network;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.network}>
			<NetworkCard item={item} />
		</ShowUpItem>
	));
}

function NetworkCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Network["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Group wrap="nowrap">
				<div>
					<Text
						fw="bold"
						lineClamp={1}
						size="md"
						title={item.network}
						tt="capitalize"
					>
						{item.network}
					</Text>

					{Boolean(item.network_block_height) && (
						<NetworkInfoRenderer
							title="Block Height"
							value={item.network_block_height}
						/>
					)}

					{Boolean(item.network_gas_price) && (
						<NetworkInfoRenderer
							decimals={9}
							title="Gas Price"
							unit="Gwei"
							value={item.network_gas_price}
						/>
					)}

					{Boolean(item.network_tx_count) && (
						<NetworkInfoRenderer
							title="Transaction Count"
							value={item.network_tx_count}
						/>
					)}

					{Boolean(item.network_tx_total) && (
						<NetworkInfoRenderer
							decimals={9}
							title="Transaction Total"
							value={item.network_tx_total}
						/>
					)}

					{Boolean(item.token_market_cap) && (
						<NetworkInfoRenderer
							decimals={2}
							title="Market Cap"
							unit="USD"
							value={item.token_market_cap}
						/>
					)}

					{Boolean(item.token_price) && (
						<NetworkInfoRenderer
							decimals={2}
							title="Token Price"
							unit="USD"
							value={item.token_price}
						/>
					)}

					{Boolean(item.token_supply) && (
						<NetworkInfoRenderer
							decimals={2}
							title="Token Supply"
							value={item.token_supply}
						/>
					)}

					{Boolean(item.token_volume) && (
						<NetworkInfoRenderer
							decimals={2}
							title="Token Volume"
							value={item.token_supply}
						/>
					)}
				</div>
			</Group>
		</Card>
	);
}

function NetworkInfoRenderer({
	decimals,
	title,
	unit,
	value,
}: {
	decimals?: number;
	title: string;
	unit?: string;
	value: number;
}) {
	return (
		<div>
			<Text size="xl">
				<Counter decimals={decimals} from={0} to={value} /> {unit}
			</Text>
			<Text fw="bold" lineClamp={1} size="xs" title={title}>
				{title}
			</Text>
		</div>
	);
}
