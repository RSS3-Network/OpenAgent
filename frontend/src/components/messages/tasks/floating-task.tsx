"use client";

import { Dialog } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

export function FloatingTask({ sessionId }: { sessionId: string }) {
	const [opened, { close, toggle }] = useDisclosure(false);

	return (
		<Dialog onClose={close} opened={opened} position={{ right: 20, top: 20 }}>
			123
		</Dialog>
	);
}
