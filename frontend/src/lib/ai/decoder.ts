import { AiSessionMessageChunkForRoleAi } from "@/server/api/routers/ai/types/session";

export function createChunkDecoder() {
	const decoder = new TextDecoder();

	return function (
		chunk: Uint8Array | undefined
	): AiSessionMessageChunkForRoleAi[] {
		if (!chunk) return [];
		const str = decoder.decode(chunk, { stream: true });
		try {
			return splitJsons(str)
				.map((a) => safeJsonParse(a))
				.filter(Boolean);
		} catch (e: any) {
			e.message = `Failed to parse chunk: ${str}`;
			e.chunk = str;
			console.error(e);
			return [];
		}
	};
}

function splitJsons(a: string) {
	return a.split("}{").map((item, index) => {
		if (a.split("}{").length > 1) {
			if (index == 0) {
				return item + "}";
			} // first msg
			else if (index < a.split("}{").length - 1) {
				return "{" + item + "}";
			} // middle msgs
			else {
				return "{" + item;
			}
		} // last msg
		else {
			return a;
		} // no need to do anything if single msg
	});
}

function safeJsonParse(a: string) {
	try {
		return JSON.parse(a);
	} catch (e: any) {
		e.message = `Failed to parse chunk: ${a}`;
		e.chunk = a;
		console.error(e);
		return undefined;
	}
}
