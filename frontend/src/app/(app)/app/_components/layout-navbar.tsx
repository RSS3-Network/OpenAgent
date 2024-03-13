"use client";

import type { DragLocationHistory } from "@atlaskit/pragmatic-drag-and-drop/types";

import { useLocalSettings } from "@/lib/settings/local";
import { draggable } from "@atlaskit/pragmatic-drag-and-drop/adapter/element";
import { cancelUnhandled } from "@atlaskit/pragmatic-drag-and-drop/addon/cancel-unhandled";
import { disableNativeDragPreview } from "@atlaskit/pragmatic-drag-and-drop/util/disable-native-drag-preview";
import { AppShellNavbar, Box, TooltipFloating } from "@mantine/core";
import { atom, useAtom } from "jotai";
import { type ReactNode, useEffect, useRef, useState } from "react";

import { useBurgerOpen } from "./layout-burger";
import classes from "./layout-navbar.module.css";

const widths = {
	max: 600,
	min: 200,
};

const navbarLocalWidthAtom = atom<null | number>(null);
export function useNavbarWidth() {
	const [initialWidth] = useLocalSettings("interface.navbar.width");
	const [intermediateWidth, setIntermediateWidth] =
		useAtom(navbarLocalWidthAtom);

	useEffect(() => {
		if (initialWidth) {
			setIntermediateWidth(initialWidth);
		}
	}, [initialWidth, setIntermediateWidth]);

	return intermediateWidth ?? initialWidth;
}

function getProposedWidth({
	initialWidth,
	location,
}: {
	initialWidth: number;
	location: DragLocationHistory;
}): number {
	const diffX = location.current.input.clientX - location.initial.input.clientX;
	const proposedWidth = initialWidth + diffX;

	// ensure we don't go below the min or above the max allowed widths
	return Math.min(Math.max(widths.min, proposedWidth), widths.max);
}

export function LayoutNavbar({ children }: { children: ReactNode }) {
	const [initialWidth, setInitialWidth] = useLocalSettings(
		"interface.navbar.width"
	);
	const [intermediateWidth, setIntermediateWidth] =
		useAtom(navbarLocalWidthAtom);
	const resizerRef = useRef<HTMLDivElement | null>(null);
	const [state, setState] = useState<{
		type: "dragging" | "idle";
	}>({
		type: "idle",
	});

	const { desktop } = useBurgerOpen();

	useEffect(() => {
		const divider = resizerRef.current;
		if (!divider) return;

		return draggable({
			element: divider,
			onDrag({ location }) {
				setIntermediateWidth(getProposedWidth({ initialWidth, location }));
			},
			onDragStart() {
				setState({ type: "dragging" });
			},
			onDrop({ location }) {
				cancelUnhandled.stop();
				setState({ type: "idle" });

				setInitialWidth(getProposedWidth({ initialWidth, location }));
			},
			onGenerateDragPreview: ({ nativeSetDragImage }) => {
				// we will be moving the line to indicate a drag
				// we can disable the native drag preview
				disableNativeDragPreview({ nativeSetDragImage });
				// we don't want any native drop animation for when the user
				// does not drop on a drop target. we want the drag to finish immediately
				cancelUnhandled.start();
			},
		});
	}, [initialWidth, setInitialWidth, setIntermediateWidth]);

	return (
		<AppShellNavbar>
			<TooltipFloating
				label={
					<>
						Drag to resize
						<br />
						Click to close
					</>
				}
				position="right"
			>
				<Box
					className={classes.resizer}
					data-dragging={state.type === "dragging"}
					onClick={() => {
						desktop[1]((v) => !v);
					}}
					ref={resizerRef}
					visibleFrom="sm"
				></Box>
			</TooltipFloating>

			{children}
		</AppShellNavbar>
	);
}
