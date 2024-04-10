import type { Instruction } from "@atlaskit/pragmatic-drag-and-drop-hitbox/tree-item";

import { AiSessionTreeItem } from "@/server/api/routers/ai/types/session";
import {
	attachInstruction,
	extractInstruction,
} from "@atlaskit/pragmatic-drag-and-drop-hitbox/tree-item";
import { DropIndicator } from "@atlaskit/pragmatic-drag-and-drop-react-indicator/tree-item";
import { createContext } from "react";

export type LocalAiSessionTreeItem = Omit<AiSessionTreeItem, "children"> & {
	children: LocalAiSessionTreeItem[];
	isOpen: boolean;
};
export type LocalAiSessionTree = LocalAiSessionTreeItem[];

type TreeAction =
	| {
			index: number;
			sessionId: string;
			targetSessionId: string;
			type: "modal-move";
	  }
	| {
			instruction: Instruction;
			sessionId: string;
			targetSessionId: string;
			type: "instruction";
	  }
	| {
			sessionId: string;
			type: "collapse";
	  }
	| {
			sessionId: string;
			type: "expand";
	  }
	| {
			sessionId: string;
			type: "toggle";
	  }
	| {
			tree: LocalAiSessionTree;
			type: "reset";
	  };

export type TreeState = {
	data: LocalAiSessionTree;
	lastAction: TreeAction | null;
};

export type TreeContextValue = {
	dispatch: (action: TreeAction) => void;
	getChildrenOfItem: (sessionId: string) => LocalAiSessionTree;
	getMoveTargets: ({ sessionId }: { sessionId: string }) => LocalAiSessionTree;
	getPathToItem: (sessionId: string) => string[];
	registerTreeItem: (args: {
		actionMenuTrigger: HTMLElement;
		element: HTMLElement;
		sessionId: string;
	}) => void;
	uniqueContextId: Symbol;
};

export const TreeContext = createContext<TreeContextValue>({
	dispatch: () => {},
	getChildrenOfItem: () => [],
	getMoveTargets: () => [],
	getPathToItem: () => [],
	registerTreeItem: () => {},
	uniqueContextId: Symbol("uniqueId"),
});

export type DependencyContext = {
	DropIndicator: typeof DropIndicator;
	attachInstruction: typeof attachInstruction;
	extractInstruction: typeof extractInstruction;
};

export const DependencyContext = createContext<DependencyContext>({
	DropIndicator: DropIndicator,
	attachInstruction: attachInstruction,
	extractInstruction: extractInstruction,
});

export const tree = {
	find(
		data: LocalAiSessionTree,
		sessionId: string
	): LocalAiSessionTreeItem | undefined {
		for (const item of data) {
			if (item.session_id === sessionId) {
				return item;
			}

			if (tree.hasChildren(item)) {
				const result = tree.find(item.children, sessionId);
				if (result) {
					return result;
				}
			}
		}
	},
	getPathToItem({
		current,
		parentIds = [],
		targetSessionId,
	}: {
		current: LocalAiSessionTree;
		parentIds?: string[];
		targetSessionId: string;
	}): string[] | undefined {
		for (const item of current) {
			if (item.session_id === targetSessionId) {
				return parentIds;
			}
			const nested = tree.getPathToItem({
				current: item.children,
				parentIds: [...parentIds, item.session_id],
				targetSessionId: targetSessionId,
			});
			if (nested) {
				return nested;
			}
		}
	},
	hasChildren(item: LocalAiSessionTreeItem): boolean {
		return item.children.length > 0;
	},
	insertAfter(
		data: LocalAiSessionTree,
		targetSessionId: string,
		newItem: LocalAiSessionTreeItem
	): LocalAiSessionTree {
		return data.flatMap((item) => {
			if (item.session_id === targetSessionId) {
				return [item, newItem];
			}

			if (tree.hasChildren(item)) {
				return {
					...item,
					children: tree.insertAfter(item.children, targetSessionId, newItem),
				};
			}

			return item;
		});
	},
	insertBefore(
		data: LocalAiSessionTree,
		targetSessionId: string,
		newItem: LocalAiSessionTreeItem
	): LocalAiSessionTree {
		return data.flatMap((item) => {
			if (item.session_id === targetSessionId) {
				return [newItem, item];
			}
			if (tree.hasChildren(item)) {
				return {
					...item,
					children: tree.insertBefore(item.children, targetSessionId, newItem),
				};
			}
			return item;
		});
	},
	insertChild(
		data: LocalAiSessionTree,
		targetSessionId: string,
		newItem: LocalAiSessionTreeItem
	): LocalAiSessionTree {
		return data.flatMap((item) => {
			if (item.session_id === targetSessionId) {
				// already a parent: add as first child
				return {
					...item,
					children: [newItem, ...item.children],
					// opening item so you can see where item landed
					isOpen: true,
				};
			}

			if (!tree.hasChildren(item)) {
				return item;
			}

			return {
				...item,
				children: tree.insertChild(item.children, targetSessionId, newItem),
			};
		});
	},
	remove(data: LocalAiSessionTree, id: string): LocalAiSessionTree {
		return data
			.filter((item) => item.session_id !== id)
			.map((item) => {
				if (tree.hasChildren(item)) {
					return {
						...item,
						children: tree.remove(item.children, id),
					};
				}
				return item;
			});
	},
};

export function treeStateReducer(
	state: TreeState,
	action: TreeAction
): TreeState {
	return {
		data: dataReducer(state.data, action),
		lastAction: action,
	};
}

const dataReducer = (data: LocalAiSessionTree, action: TreeAction) => {
	console.log("action", action);

	if (action.type === "reset") {
		return action.tree;
	}

	const item = tree.find(data, action.sessionId);
	if (!item) {
		return data;
	}

	if (action.type === "instruction") {
		const instruction = action.instruction;

		if (instruction.type === "reparent") {
			const path = tree.getPathToItem({
				current: data,
				targetSessionId: action.targetSessionId,
			});
			if (!path) {
				throw new Error("Could not find path to item");
			}
			const desiredId = path[instruction.desiredLevel];
			let result = tree.remove(data, action.sessionId);
			result = tree.insertAfter(result, desiredId, item);
			return result;
		}

		// the rest of the actions require you to drop on something else
		if (action.sessionId === action.targetSessionId) {
			return data;
		}

		if (instruction.type === "reorder-above") {
			let result = tree.remove(data, action.sessionId);
			result = tree.insertBefore(result, action.targetSessionId, item);
			return result;
		}

		if (instruction.type === "reorder-below") {
			let result = tree.remove(data, action.sessionId);
			result = tree.insertAfter(result, action.targetSessionId, item);
			return result;
		}

		if (instruction.type === "make-child") {
			let result = tree.remove(data, action.sessionId);
			result = tree.insertChild(result, action.targetSessionId, item);
			return result;
		}

		console.warn("TODO: action not implemented", instruction);

		return data;
	}

	function toggle(item: LocalAiSessionTreeItem): LocalAiSessionTreeItem {
		if (!tree.hasChildren(item) || action.type === "reset") {
			return item;
		}

		if (item.session_id === action.sessionId) {
			return { ...item, isOpen: !item.isOpen };
		}

		return { ...item, children: item.children.map(toggle) };
	}

	if (action.type === "toggle") {
		return data.map(toggle);
	}

	if (action.type === "expand") {
		if (tree.hasChildren(item) && !item.isOpen) {
			return data.map(toggle);
		}
		return data;
	}

	if (action.type === "collapse") {
		if (tree.hasChildren(item) && item.isOpen) {
			return data.map(toggle);
		}
		return data;
	}

	if (action.type === "modal-move") {
		let result = tree.remove(data, item.session_id);

		const siblingItems = getChildItems(result, action.targetSessionId);

		if (siblingItems.length === 0) {
			if (action.targetSessionId === "") {
				/**
				 * If the target is the root level, and there are no siblings, then
				 * the item is the only thing in the root level.
				 */
				result = [item];
			} else {
				/**
				 * Otherwise for deeper levels that have no children, we need to
				 * use `insertChild` instead of inserting relative to a sibling.
				 */
				result = tree.insertChild(result, action.targetSessionId, item);
			}
		} else if (action.index === siblingItems.length) {
			const relativeTo = siblingItems[siblingItems.length - 1];
			/**
			 * If the position selected is the end, we insert after the last item.
			 */
			result = tree.insertAfter(result, relativeTo.session_id, item);
		} else {
			const relativeTo = siblingItems[action.index];
			/**
			 * Otherwise we insert before the existing item in the given position.
			 * This results in the new item being in that position.
			 */
			result = tree.insertBefore(result, relativeTo.session_id, item);
		}

		return result;
	}

	return data;
};

function getChildItems(data: LocalAiSessionTree, targetId: string) {
	/**
	 * An empty string is representing the root
	 */
	if (targetId === "") {
		return data;
	}

	const targetItem = tree.find(data, targetId);
	if (!targetItem) {
		throw new Error("Could not find target item");
	}

	return targetItem.children;
}
