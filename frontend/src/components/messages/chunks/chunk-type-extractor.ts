export function isChunkTypeof<T extends AiSessionMessageChunkForRoleAi["type"]>(
	chunk: AiSessionMessageChunkForRoleAi,
	type: T
): chunk is AiSessionMessageChunkForRoleAi<T>;
export function isChunkTypeof<T extends AiSessionMessageChunkForRoleAi["type"]>(
	chunk: OmitMessageId<AiSessionMessageChunkForRoleAi>,
	type: T
): chunk is OmitMessageId<AiSessionMessageChunkForRoleAi<T>>;
export function isChunkTypeof<T extends AiSessionMessageChunkForRoleAi["type"]>(
	chunk:
		| AiSessionMessageChunkForRoleAi
		| OmitMessageId<AiSessionMessageChunkForRoleAi>,
	type: T
): chunk is
	| AiSessionMessageChunkForRoleAi<T>
	| OmitMessageId<AiSessionMessageChunkForRoleAi<T>> {
	return chunk?.type === type;
}

export function isChunkToolTypeOf<T extends AiSessionMessageToolType>(
	chunk: AiSessionMessageTool,
	type: T
): chunk is AiSessionMessageTool<T>;
export function isChunkToolTypeOf<T extends AiSessionMessageToolType>(
	chunk: OmitMessageId<AiSessionMessageTool>,
	type: T
): chunk is OmitMessageId<AiSessionMessageTool<T>>;
export function isChunkToolTypeOf<T extends AiSessionMessageToolType>(
	chunk: AiSessionMessageTool | OmitMessageId<AiSessionMessageTool>,
	type: T
): chunk is AiSessionMessageTool<T> | OmitMessageId<AiSessionMessageTool<T>> {
	// @ts-ignore TODO: fix this
	if (chunk.body.tool_name === "nft" && type === "collection") {
		return true;
	}
	return chunk.body.tool_name === type;
}

export function isChunkToolTypeofTask(
	chunk: AiSessionMessageChunkForRoleAi
): chunk is AiSessionMessageTool<"transfer">;
export function isChunkToolTypeofTask(
	chunk: OmitMessageId<AiSessionMessageChunkForRoleAi>
): chunk is OmitMessageId<AiSessionMessageTool<"transfer">>;
export function isChunkToolTypeofTask(
	chunk:
		| AiSessionMessageChunkForRoleAi
		| OmitMessageId<AiSessionMessageChunkForRoleAi>
): chunk is
	| AiSessionMessageTool<"transfer">
	| OmitMessageId<AiSessionMessageTool<"transfer">> {
	return isChunkTypeof(chunk, "tool") && isChunkToolTypeOf(chunk, "transfer");
}
