"use client";

import {
	Group,
	ScrollArea as ScrollArea_,
	ScrollAreaProps,
	Stack,
} from "@mantine/core";
import { AnimatePresence, m } from "framer-motion";
import { useLayoutEffect, useRef, useState } from "react";

import classes from "./scroll-area.module.css";

export function ScrollArea({
	children,
	orientation = "horizontal",
	...props
}: {
	children: React.ReactNode;
	orientation?: "horizontal" | "vertical";
} & ScrollAreaProps) {
	const viewport = useRef<HTMLDivElement>(null);
	const [scrollPosition, onScrollPositionChange] = useState({ x: 0, y: 0 });
	const [isScrolledToBottom, setIsScrolledToBottom] = useState(true);

	const xOrY = orientation === "horizontal" ? "x" : "y";

	const isScrolledToTop = scrollPosition[xOrY] === 0;

	// console.log({
	// 	clientWidth: viewport.current?.clientWidth,
	// 	isScrolledToBottom,
	// 	scrollPosition: scrollPosition[xOrY],
	// 	scrollWidth: viewport.current?.scrollWidth,
	// });

	useLayoutEffect(() => {
		if (viewport.current) {
			setIsScrolledToBottom(
				viewport.current &&
					scrollPosition[xOrY] + 1 >=
						viewport.current?.[
							orientation === "horizontal" ? "scrollWidth" : "scrollHeight"
						] -
							viewport.current?.[
								orientation === "horizontal" ? "clientWidth" : "clientHeight"
							]
			);
		}
	}, [orientation, scrollPosition, xOrY]);

	return (
		<ScrollArea_
			onScrollPositionChange={onScrollPositionChange}
			type="never"
			viewportRef={viewport}
			{...props}
		>
			<AnimatePresence>
				{!isScrolledToTop && (
					<m.div
						animate={{ opacity: 1 }}
						className={
							orientation === "horizontal"
								? classes["mask-l"]
								: classes["mask-t"]
						}
						exit={{ opacity: 0 }}
						initial={{ opacity: 0 }}
					></m.div>
				)}
			</AnimatePresence>
			{orientation === "horizontal" ? (
				<Group align="stretch" gap="xs" justify="space-between" wrap="nowrap">
					{children}
				</Group>
			) : (
				<Stack align="stretch" gap="xs" justify="space-between">
					{children}
				</Stack>
			)}
			<AnimatePresence>
				{!isScrolledToBottom && (
					<m.div
						animate={{ opacity: 1 }}
						className={
							orientation === "horizontal"
								? classes["mask-r"]
								: classes["mask-b"]
						}
						exit={{ opacity: 0 }}
						initial={{ opacity: 0 }}
					></m.div>
				)}
			</AnimatePresence>
		</ScrollArea_>
	);
}
