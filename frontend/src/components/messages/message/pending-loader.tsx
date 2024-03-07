"use client";

import { useAskAiStatus, useCurrentSessionId } from "@/lib/ai/hooks";
import { Loader } from "@mantine/core";

export function PendingLoader({ isLastMessage }: { isLastMessage: boolean }) {
	const { currentSessionId } = useCurrentSessionId();
	const { status } = useAskAiStatus({ sessionId: currentSessionId! });

	const isPending = status === "pending" && isLastMessage;

	return isPending ? (
		<p>
			<Loader size="sm" type="dots" />
		</p>
	) : (
		<></>
	);
}
