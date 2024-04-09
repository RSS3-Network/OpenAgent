import { Anchor, Text } from "@mantine/core";
import { IconBulb } from "@tabler/icons-react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useSnapshot } from "valtio";

import { ScrollArea } from "../basics/scroll-area";
import { isChunkToolTypeOf } from "../chunk-type-extractor";
import { ToolChunkLoading } from "./loading";
import { ToolChunkNotFound } from "./notfound";

const ToolChunkError = dynamic(() =>
	import("./error").then((mod) => mod.ToolChunkError)
);
const ToolChunkAccount = dynamic(() =>
	import("./account").then((mod) => mod.ToolChunkAccount)
);
const ToolChunkCollection = dynamic(() =>
	import("./collection").then((mod) => mod.ToolChunkCollection)
);
const ToolChunkDapp = dynamic(() =>
	import("./dapp").then((mod) => mod.ToolChunkDapp)
);
const ToolChunkDefi = dynamic(() =>
	import("./defi").then((mod) => mod.ToolChunkDefi)
);
const ToolChunkFeed = dynamic(() =>
	import("./feed").then((mod) => mod.ToolChunkFeed)
);
const ToolChunkNetwork = dynamic(() =>
	import("./network").then((mod) => mod.ToolChunkNetwork)
);
const ToolChunkSwap = dynamic(() =>
	import("./swap").then((mod) => mod.ToolChunkSwap)
);
const ToolChunkToken = dynamic(() =>
	import("./token").then((mod) => mod.ToolChunkToken)
);
const ToolChunkExecutor = dynamic(() =>
	import("./executor").then((mod) => mod.ToolChunkExecutor)
);
const ToolChunkTransfer = dynamic(() =>
	import("./transfer").then((mod) => mod.ToolChunkTransfer)
);

export function ToolChunk({
	chunk,
}: {
	chunk: OmitMessageId<AiSessionMessageTool>;
}) {
	const snap = useSnapshot(chunk) as typeof chunk;

	const shouldShowRss3 = !["swap", "transfer"].includes(snap.body.tool_name);

	return (
		<div>
			<ScrollArea py="sm">
				<ToolChunkBody chunk={snap} />
			</ScrollArea>

			{shouldShowRss3 && (
				<Text c="dimmed" size="xs">
					<IconBulb className="align-text-bottom" size="1rem" /> Data powered by{" "}
					<Anchor component={Link} href="https://rss3.io" target="_blank">
						RSS3
					</Anchor>
				</Text>
			)}
		</div>
	);
}

function ToolChunkBody({
	chunk,
}: {
	chunk: OmitMessageId<AiSessionMessageTool>;
}) {
	if (!("output" in chunk.body) || !chunk.body.output) {
		return <ToolChunkLoading body={chunk.body.input} />;
	}

	if (chunk.body.output.error) {
		return (
			<ToolChunkError
				body={chunk.body.output as AiSessionMessageToolOutputBody_Error}
			/>
		);
	}

	if (
		!chunk.body.output ||
		("data" in chunk.body.output && !chunk.body.output.data.items)
	) {
		return <ToolChunkNotFound />;
	}

	if ("error" in chunk.body.output) {
		return <>Something Wrong</>;
	}

	if (isChunkToolTypeOf(chunk, "account")) {
		return <ToolChunkAccount body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "collection")) {
		return <ToolChunkCollection body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "dapp")) {
		return <ToolChunkDapp body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "defi")) {
		return <ToolChunkDefi body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "feed")) {
		return <ToolChunkFeed body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "network")) {
		return <ToolChunkNetwork body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "token")) {
		return <ToolChunkToken body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "executor")) {
		return <ToolChunkExecutor body={chunk.body.output} />;
	}

	if (isChunkToolTypeOf(chunk, "transfer")) {
		return (
			<ToolChunkTransfer
				body={chunk.body.output}
				expired={!chunk.body.still_valid}
			/>
		);
	}

	if (isChunkToolTypeOf(chunk, "swap")) {
		return (
			<ToolChunkSwap
				body={chunk.body.output}
				expired={!chunk.body.still_valid}
			/>
		);
	}

	return <></>;
}
