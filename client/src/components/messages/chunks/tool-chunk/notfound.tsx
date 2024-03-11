import { Card, Group, Text } from "@mantine/core";

import { ShowUpItem } from "../basics/show-up-item";

export function ToolChunkNotFound() {
	return (
		<ShowUpItem index={0}>
			<Card>
				<Group wrap="nowrap">
					<div>
						<Text fw="bold" lineClamp={1} size="xs">
							Found nothing...
						</Text>
					</div>
				</Group>
			</Card>
		</ShowUpItem>
	);
}
