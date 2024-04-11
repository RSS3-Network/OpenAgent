import { AiSessionMessageToolOutputBody_Token } from "@/server/api/routers/ai/types/session";
import { Card, Divider, Group, Image, Text } from "@mantine/core";

import { ActionIconCopy, ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { Counter } from "../basics/counter";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkToken({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Token;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.token_address}>
			<TokenCard item={item} />
		</ShowUpItem>
	));
}

function TokenCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Token["data"]["items"][0];
}) {
	// console.log(item);
	return (
		<Card>
			<Group align="flex-start" wrap="nowrap">
				{Boolean(item.token_logo) && (
					<Image
						alt="Token logo"
						h={60}
						radius="md"
						src={item.token_logo}
						w={60}
					/>
				)}

				<div>
					{Boolean(item.token_name) && (
						<Group gap="xs" wrap="nowrap">
							<Text fw="bold" size="md" title={item.network} tt="capitalize">
								{item.token_name}
							</Text>
							<Text tt="uppercase">({item.token_symbol})</Text>
						</Group>
					)}
					<Text
						lineClamp={2}
						size="xs"
						title={item.token_description}
						w="20rem"
					>
						{item.token_description}
					</Text>

					{Boolean(item.token_address) &&
						item.token_address !==
							"0x0000000000000000000000000000000000000000" && (
							<Group gap="xs" wrap="nowrap">
								<Address address={item.token_address} />
								<ActionIconCopy value={item.token_address} />
								<ActionIconExternalLink
									href={`https://hoot.it/token/${item.token_address}`}
									label="View on Hoot.it"
								/>
							</Group>
						)}

					<Divider />

					{Boolean(item.token_market_cap) && (
						<TokenInfoRenderer
							decimals={2}
							title="Market Cap"
							unit="USD"
							value={item.token_market_cap}
						/>
					)}

					{Boolean(item.token_market_cap_change_24h) && (
						<TokenInfoRenderer
							decimals={2}
							title="Market Cap Change (24h)"
							unit="USD"
							value={item.token_market_cap_change_24h}
						/>
					)}

					{Boolean(item.token_price) && (
						<TokenInfoRenderer
							decimals={2}
							title="Token Price"
							unit="USD"
							value={item.token_price}
						/>
					)}

					{Boolean(item.token_price_change_24h) && (
						<TokenInfoRenderer
							decimals={2}
							title="Token Price Change (24h)"
							unit="USD"
							value={item.token_price_change_24h}
						/>
					)}

					{Boolean(item.token_price_high_24h) && (
						<TokenInfoRenderer
							decimals={2}
							title="Token Price High (24h)"
							unit="USD"
							value={item.token_price_high_24h}
						/>
					)}

					{Boolean(item.token_price_low_24h) && (
						<TokenInfoRenderer
							decimals={2}
							title="Token Price Low (24h)"
							unit="USD"
							value={item.token_price_low_24h}
						/>
					)}
				</div>
			</Group>
		</Card>
	);
}

function TokenInfoRenderer({
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
