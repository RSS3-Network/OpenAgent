"use client";

import {
	draggable,
	dropTargetForElements,
	monitorForElements,
} from "@atlaskit/pragmatic-drag-and-drop/adapter/element";
import { DragLocationHistory } from "@atlaskit/pragmatic-drag-and-drop/dist/types/internal-types";
import { combine } from "@atlaskit/pragmatic-drag-and-drop/util/combine";
import { offsetFromPointer } from "@atlaskit/pragmatic-drag-and-drop/util/offset-from-pointer";
import { setCustomNativeDragPreview } from "@atlaskit/pragmatic-drag-and-drop/util/set-custom-native-drag-preview";
import {
	Instruction,
	ItemMode,
} from "@atlaskit/pragmatic-drag-and-drop-hitbox/dist/types/tree-item";
import { Box } from "@mantine/core";
import { useCallback, useContext, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";

import { SessionLink } from "./session-link";
import {
	DependencyContext,
	LocalAiSessionTreeItem,
	TreeContext,
} from "./tree-context";

function getParentLevelOfInstruction(instruction: Instruction): number {
	if (instruction.type === "instruction-blocked") {
		return getParentLevelOfInstruction(instruction.desired);
	}
	if (instruction.type === "reparent") {
		return instruction.desiredLevel - 1;
	}
	return instruction.currentLevel - 1;
}

function delay({
	fn,
	waitMs: timeMs,
}: {
	fn: () => void;
	waitMs: number;
}): () => void {
	let timeoutId: null | number = window.setTimeout(() => {
		timeoutId = null;
		fn();
	}, timeMs);
	return function cancel() {
		if (timeoutId) {
			window.clearTimeout(timeoutId);
			timeoutId = null;
		}
	};
}

const indentPerLevel = 5;

export function SessionLinkTreeItem({
	item,
	level,
	mode,
}: {
	item: LocalAiSessionTreeItem;
	level: number;
	mode: ItemMode;
}) {
	const buttonRef = useRef<HTMLDivElement>(null);

	const [state, setState] = useState<
		"dragging" | "idle" | "parent-of-instruction" | "preview"
	>("idle");
	const [instruction, setInstruction] = useState<Instruction | null>(null);
	const cancelExpandRef = useRef<(() => void) | null>(null);

	const { dispatch, getPathToItem, registerTreeItem, uniqueContextId } =
		useContext(TreeContext);
	const { DropIndicator, attachInstruction, extractInstruction } =
		useContext(DependencyContext);
	const toggleOpen = useCallback(() => {
		dispatch({ sessionId: item.session_id, type: "toggle" });
	}, [dispatch, item]);

	const actionMenuTriggerRef = useRef<HTMLButtonElement>(null);
	useEffect(() => {
		if (!buttonRef.current || !actionMenuTriggerRef.current) {
			return;
		}
		return registerTreeItem({
			actionMenuTrigger: actionMenuTriggerRef.current,
			element: buttonRef.current,
			sessionId: item.session_id,
		});
	}, [item.session_id, registerTreeItem]);

	const cancelExpand = useCallback(() => {
		cancelExpandRef.current?.();
		cancelExpandRef.current = null;
	}, []);

	const clearParentOfInstructionState = useCallback(() => {
		setState((current) =>
			current === "parent-of-instruction" ? "idle" : current
		);
	}, []);

	// When an item has an instruction applied
	// we are highlighting it's parent item for improved clarity
	const shouldHighlightParent = useCallback(
		(location: DragLocationHistory): boolean => {
			const target = location.current.dropTargets[0];

			if (!target) {
				return false;
			}

			const instruction = extractInstruction(target.data);

			if (!instruction) {
				return false;
			}

			const targetId = target.data.id;
			if (typeof targetId !== "string") {
				throw new Error("targetId is not a string");
			}

			const path = getPathToItem(targetId);
			const parentLevel: number = getParentLevelOfInstruction(instruction);
			const parentId = path[parentLevel];
			return parentId === item.session_id;
		},
		[getPathToItem, extractInstruction, item]
	);

	useEffect(() => {
		if (!buttonRef.current) {
			return;
		}

		function updateIsParentOfInstruction({
			location,
		}: {
			location: DragLocationHistory;
		}) {
			if (shouldHighlightParent(location)) {
				setState("parent-of-instruction");
				return;
			}
			clearParentOfInstructionState();
		}

		return combine(
			draggable({
				element: buttonRef.current,
				getInitialData: () => ({
					id: item.session_id,
					isOpenOnDragStart: item.isOpen,
					type: "tree-item",
					uniqueContextId,
				}),
				onDragStart: ({ source }) => {
					setState("dragging");
					// collapse open items during a drag
					if (source.data.isOpenOnDragStart) {
						dispatch({ sessionId: item.session_id, type: "collapse" });
					}
				},
				onDrop: ({ source }) => {
					setState("idle");
					if (source.data.isOpenOnDragStart) {
						dispatch({ sessionId: item.session_id, type: "expand" });
					}
				},
				onGenerateDragPreview: ({ nativeSetDragImage }) => {
					// setCustomNativeDragPreview({
					// 	getOffset: offsetFromPointer({ x: "16px", y: "8px" }),
					// 	nativeSetDragImage,
					// 	render: ({ container }) => {
					// 		const root = createRoot(container);
					// 		root.render(<SessionLink session={item} />);
					// 		return () => root.unmount();
					// 	},
					// });
				},
			}),
			dropTargetForElements({
				canDrop: ({ source }) =>
					source.data.type === "tree-item" &&
					source.data.uniqueContextId === uniqueContextId,
				element: buttonRef.current,
				getData: ({ element, input }) => {
					const data = { id: item.session_id };

					return attachInstruction(data, {
						// block: item.isDraft ? ["make-child"] : [],
						block: [],
						currentLevel: level,
						element,
						indentPerLevel,
						input,
						mode,
					});
				},
				getIsSticky: () => true,
				onDrag: ({ self, source }) => {
					const instruction = extractInstruction(self.data);

					console.log({ source });
					if (source.data.id !== item.session_id) {
						// expand after 500ms if still merging
						if (
							instruction?.type === "make-child" &&
							item.children.length &&
							!item.isOpen &&
							!cancelExpandRef.current
						) {
							cancelExpandRef.current = delay({
								fn: () =>
									dispatch({ sessionId: item.session_id, type: "expand" }),
								waitMs: 500,
							});
						}
						if (instruction?.type !== "make-child" && cancelExpandRef.current) {
							cancelExpand();
						}

						setInstruction(instruction);
						return;
					}
					if (instruction?.type === "reparent") {
						setInstruction(instruction);
						return;
					}
					setInstruction(null);
				},
				onDragLeave: () => {
					cancelExpand();
					setInstruction(null);
				},
				onDrop: () => {
					cancelExpand();
					setInstruction(null);
				},
			}),
			monitorForElements({
				canMonitor: ({ source }) =>
					source.data.uniqueContextId === uniqueContextId,
				onDrag: updateIsParentOfInstruction,
				onDragStart: updateIsParentOfInstruction,
				onDrop() {
					clearParentOfInstructionState();
				},
			})
		);
	}, [
		dispatch,
		item,
		mode,
		level,
		cancelExpand,
		uniqueContextId,
		extractInstruction,
		attachInstruction,
		getPathToItem,
		clearParentOfInstructionState,
		shouldHighlightParent,
	]);

	useEffect(
		function mount() {
			return function unmount() {
				cancelExpand();
			};
		},
		[cancelExpand]
	);

	const aria = (() => {
		if (!item.children.length) {
			return undefined;
		}
		return {
			"aria-controls": `tree-item-${item.session_id}--subtree`,
			"aria-expanded": item.isOpen,
		};
	})();

	const [isMoveDialogOpen, setIsMoveDialogOpen] = useState(false);
	const openMoveDialog = useCallback(() => {
		setIsMoveDialogOpen(true);
	}, []);
	const closeMoveDialog = useCallback(() => {
		setIsMoveDialogOpen(false);
	}, []);

	return (
		<Box ml={level * indentPerLevel} ref={buttonRef}>
			{/* {state} */}
			<SessionLink session={item} />
			{instruction ? <DropIndicator instruction={instruction} /> : null}

			{item.children.length && item.isOpen ? (
				<div>
					{item.children.map((child, index, array) => {
						const childType: ItemMode = (() => {
							if (child.children.length && child.isOpen) {
								return "expanded";
							}

							if (index === array.length - 1) {
								return "last-in-group";
							}

							return "standard";
						})();
						return (
							<SessionLinkTreeItem
								item={child}
								key={child.session_id}
								level={level + 1}
								mode={childType}
							/>
						);
					})}
				</div>
			) : null}
		</Box>
	);
}
