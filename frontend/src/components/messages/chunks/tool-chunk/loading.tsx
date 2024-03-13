import { Card, Group, Loader, Text } from "@mantine/core";
import { m } from "framer-motion";

export function ToolChunkLoading({
	body,
}: {
	body: AiSessionMessageToolInputBody;
}) {
	return (
		<Card>
			<Group wrap="nowrap">
				<Loader size="sm" type="dots" />

				<m.span
					animate={{
						opacity: [0.3, 1, 1, 0.3],
					}}
					transition={{
						duration: 2,
						repeat: Infinity,
						repeatType: "loop",
					}}
				>
					<Text span>Querying...</Text>
				</m.span>
			</Group>
		</Card>
	);
}
