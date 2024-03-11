"use client";

import { rem } from "@mantine/core";
import { Spotlight as Spotlight_ } from "@mantine/spotlight";
import { IconCommand } from "@tabler/icons-react";

import { useActions } from "./actions";

export function Spotlight() {
	const { actions } = useActions();
	return (
		<>
			<Spotlight_
				actions={actions}
				highlightQuery
				nothingFound="Nothing found..."
				// limit={7}
				scrollable
				searchProps={{
					leftSection: (
						<IconCommand
							stroke={1.5}
							style={{ height: rem(20), width: rem(20) }}
						/>
					),
					placeholder: "Type a command or search...",
				}}
				shortcut={[]}
				tagsToIgnore={[]}
			/>
		</>
	);
}
