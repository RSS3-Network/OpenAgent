import type { Activity, Theme } from "@rss3/js-sdk";

import { Card, Image, Text, px } from "@mantine/core";
import { useElementSize } from "@mantine/hooks";
import { tokenizeToActions } from "@rss3/js-sdk/lib/readable/activity/index";
import { Children, ReactNode } from "react";

import { ActionIconExternalLink } from "../basics/action-icon";
import { Address } from "../basics/address";
import { ScrollArea } from "../basics/scroll-area";
import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkFeed({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Feed;
}) {
	return body.data.items?.map((item, key) => (
		<ShowUpItem index={key} key={item.id}>
			<FeedCard item={item} />
		</ShowUpItem>
	));
}

function safeImageLink(src: string, size: number | string) {
	const s = px(size);
	return `https://thumbor.rss3.dev/unsafe/${s}x${s}/${src}`;
}

// https://github.com/naturalselectionlabs/hoot/blob/stg/components/account/common/card.tsx
const themeHTML: Theme<ReactNode> = {
	address: (c, m) => <Address address={c as `0x${string}`} span />,
	assetImage: (c) =>
		c ? (
			<Image
				alt="image"
				display="inline"
				h="1rem"
				src={safeImageLink(c, "1rem")}
				w="1rem"
			/>
		) : (
			""
		),
	html: (c) => "",
	image: (c) =>
		c ? (
			<Image
				alt="image"
				display="inline"
				h="1rem"
				src={safeImageLink(c, "1rem")}
				w="1rem"
			/>
		) : (
			""
		),
	name: (c) => <Text span>{c}</Text>,
	network: (c) => <Text span>{c}</Text>,
	number: (c) => <Text span>{c}</Text>,
	platform: (c) => c,
	separator: () => "",
	symbol: (c) => <Text span>{c}</Text>,
	symbolImage: (c) =>
		c ? (
			<Image
				alt="token"
				display="inline"
				h="1rem"
				src={safeImageLink(c, "1rem")}
				w="1rem"
			/>
		) : (
			""
		),
	text: (c) => c,
	time: (c) => c,
	unknown: (c) => c,
};

function FeedCard({
	item,
}: {
	item: AiSessionMessageToolOutputBody_Feed["data"]["items"][0];
}) {
	// console.log(item);

	const { height, ref } = useElementSize();

	const list = tokenizeToActions(item as unknown as Activity);

	const Inside = () =>
		list.map((ts, i) => {
			return (
				<Card key={i} w={300}>
					<Text lineClamp={5}>
						{Children.toArray(
							ts.map((t) => themeHTML[t.type](t.content, t.meta))
						)}
						<ActionIconExternalLink
							href={`https://hoot.it/${item.owner || item.from}/activity/${
								item.id
							}`}
							label="View on Hoot.it"
						/>
					</Text>
				</Card>
			);
		});

	if (list.length > 1) {
		return (
			<>
				<div ref={ref} />
				<ScrollArea mah={height} orientation="vertical">
					<Inside />
				</ScrollArea>
			</>
		);
	} else {
		return <Inside />;
	}
}
