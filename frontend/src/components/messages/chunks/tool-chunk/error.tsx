import { Card, Group, Text } from "@mantine/core";

import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkError({
	body,
}: {
	body: AiSessionMessageToolOutputBody_Error;
}) {
	return (
		<ShowUpItem index={0}>
			<Card>
				<Group wrap="nowrap">
					<div>
						<Text ff="monospace" fw="bold" size="xs" tt="uppercase">
							{body.error.code}
						</Text>
						<Text size="sm">{body.error.message}</Text>
					</div>
				</Group>
			</Card>
		</ShowUpItem>
	);
}
