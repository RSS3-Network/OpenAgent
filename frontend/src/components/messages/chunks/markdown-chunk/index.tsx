import { Markdown } from "@/components/markdown";
import { useSnapshot } from "valtio";

export function MarkdownChunk({
	chunk,
}: {
	chunk: OmitMessageId<AiSessionMessageNaturalLanguage>;
}) {
	const c = useSnapshot(chunk);
	return <Markdown>{c.body}</Markdown>;
}
