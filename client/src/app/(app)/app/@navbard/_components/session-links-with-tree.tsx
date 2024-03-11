"use client";

import { api } from "@/lib/trpc/client";
import { triggerPostMoveFlash } from "@atlaskit/pragmatic-drag-and-drop-flourish/trigger-post-move-flash";
import { ItemMode } from "@atlaskit/pragmatic-drag-and-drop-hitbox/dist/types/tree-item";
import { Divider, Text } from "@mantine/core";
import {
	useCallback,
	useContext,
	useEffect,
	useMemo,
	useReducer,
	useRef,
	useState,
} from "react";

import { SessionLink, SessionLinkSkeleton } from "./session-link";
import { SessionLinkTreeItem } from "./session-link-tree-item";
import {
	DependencyContext,
	LocalAiSessionTree,
	LocalAiSessionTreeItem,
	TreeContext,
	TreeContextValue,
	tree,
	treeStateReducer,
} from "./tree-context";

type CleanupFn = () => void;
function createTreeItemRegistry() {
	const registry = new Map<
		string,
		{ actionMenuTrigger: HTMLElement; element: HTMLElement }
	>();

	const registerTreeItem = ({
		actionMenuTrigger,
		element,
		sessionId,
	}: {
		actionMenuTrigger: HTMLElement;
		element: HTMLElement;
		sessionId: string;
	}): CleanupFn => {
		registry.set(sessionId, { actionMenuTrigger, element });
		return () => {
			registry.delete(sessionId);
		};
	};

	return { registerTreeItem, registry };
}

export function SessionLinks() {
	const [recents] = api.ai.sessions.recents.useSuspenseInfiniteQuery(
		{},
		{
			getNextPageParam: (lastPage) => lastPage.nextCursor,
			staleTime: 3000,
		}
	);

	const flattenedRecents = recents?.pages.flatMap((page) => page.result) ?? [];

	const [favorites] = api.ai.sessions.favorites.useSuspenseQuery();

	/////////

	const localTree = useMemo(() => {
		const traverse = (data: AiSessionTree): LocalAiSessionTree => {
			const result: LocalAiSessionTree = [];
			for (const item of data) {
				result.push({
					...item,
					children: traverse(item.children),
					isOpen: false,
				});
			}
			return result;
		};

		return traverse(favorites.result);
	}, [favorites.result]);

	useEffect(() => {
		updateState({ tree: localTree, type: "reset" });
	}, [localTree]);

	const [state, updateState] = useReducer(treeStateReducer, null, () => ({
		data: localTree,
		lastAction: null,
	}));
	const ref = useRef<HTMLDivElement>(null);
	const { extractInstruction } = useContext(DependencyContext);

	const [{ registerTreeItem, registry }] = useState(createTreeItemRegistry);

	const { data, lastAction } = state;
	let lastStateRef = useRef<LocalAiSessionTreeItem[]>(data);
	useEffect(() => {
		lastStateRef.current = data;
	}, [data]);

	useEffect(() => {
		if (lastAction === null) {
			return;
		}

		if (lastAction.type === "modal-move") {
			const parentName =
				lastAction.targetSessionId === ""
					? "the root"
					: `Item ${lastAction.targetSessionId}`;

			console.log(
				`You've moved Item ${lastAction.sessionId} to position ${
					lastAction.index + 1
				} in ${parentName}.`
			);

			const { actionMenuTrigger, element } =
				registry.get(lastAction.sessionId) ?? {};
			if (element) {
				triggerPostMoveFlash(element);
			}

			/**
			 * Only moves triggered by the modal will result in focus being
			 * returned to the trigger.
			 */
			actionMenuTrigger?.focus();

			return;
		}

		if (lastAction.type === "instruction") {
			const { element } = registry.get(lastAction.sessionId) ?? {};
			if (element) {
				triggerPostMoveFlash(element);
			}

			return;
		}
	}, [lastAction, registry]);

	/**
	 * Returns the items that the item with `itemId` can be moved to.
	 *
	 * Uses a depth-first search (DFS) to compile a list of possible targets.
	 */
	const getMoveTargets = useCallback(({ sessionId }: { sessionId: string }) => {
		const data = lastStateRef.current;

		const targets = [];

		const searchStack = Array.from(data);
		while (searchStack.length > 0) {
			const node = searchStack.pop();

			if (!node) {
				continue;
			}

			/**
			 * If the current node is the item we want to move, then it is not a valid
			 * move target and neither are its children.
			 */
			if (node.session_id === sessionId) {
				continue;
			}

			/**
			 * Draft items cannot have children.
			 */
			// if (node.isDraft) {
			// 	continue;
			// }

			targets.push(node);

			node.children.forEach((childNode) => searchStack.push(childNode));
		}

		return targets;
	}, []);

	const getChildrenOfItem = useCallback((itemId: string) => {
		const data = lastStateRef.current;

		/**
		 * An empty string is representing the root
		 */
		if (itemId === "") {
			return data;
		}

		const item = tree.find(data, itemId);
		if (!item) throw new Error("Could not find item");
		return item.children;
	}, []);

	const context = useMemo<TreeContextValue>(
		() => ({
			dispatch: updateState,
			getChildrenOfItem,
			// memoizing this function as it is called by all tree items repeatedly
			// An ideal refactor would be to update our data shape
			getMoveTargets,
			// to allow quick lookups of parents
			getPathToItem: (targetSessionId: string) =>
				tree.getPathToItem({
					current: lastStateRef.current,
					targetSessionId,
				}) ?? [],
			registerTreeItem,
			uniqueContextId: Symbol("unique-id"),
		}),
		[getChildrenOfItem, getMoveTargets, registerTreeItem]
	);

	return (
		<TreeContext.Provider value={context}>
			<Text c="dimmed" p="xs" size="xs">
				Favorites
			</Text>

			<div id="tree" ref={ref}>
				{data.map((item, index, array) => {
					const type: ItemMode = (() => {
						if (item.children.length && item.isOpen) {
							return "expanded";
						}

						if (index === array.length - 1) {
							return "last-in-group";
						}

						return "standard";
					})();

					return (
						<SessionLinkTreeItem
							item={item}
							key={item.session_id}
							level={0}
							mode={type}
						/>
					);
				})}
			</div>

			<Divider />

			<Text c="dimmed" p="xs" size="xs">
				Recent
			</Text>

			{flattenedRecents.map((session) => (
				<SessionLink key={session.session_id} session={session} />
			))}
		</TreeContext.Provider>
	);
}

export function SessionLinksSkeleton() {
	return (
		<>
			<SessionLinkSkeleton />
			<SessionLinkSkeleton />
			<SessionLinkSkeleton />
			<SessionLinkSkeleton />
			<SessionLinkSkeleton />
		</>
	);
}
