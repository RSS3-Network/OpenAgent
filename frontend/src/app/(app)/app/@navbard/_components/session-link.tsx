"use client";

import {
	useAiIsCurrentSession,
	useAiNewSessionRouter,
	useAiSessionTitle,
} from "@/lib/ai/hooks";
import { api } from "@/lib/trpc/client";
import { AiSessionListItem } from "@/server/api/routers/ai/types/session";
import {
	ActionIcon,
	Group,
	NavLink,
	Popover,
	PopoverDropdown,
	PopoverTarget,
	Skeleton,
	Text,
	Tooltip,
} from "@mantine/core";
import { useHover } from "@mantine/hooks";
import {
	IconCheck,
	IconDots,
	IconLink,
	IconMessageCircle,
	IconPencil,
	IconTrash,
} from "@tabler/icons-react";
import { AnimatePresence, m } from "framer-motion";
import { useContextMenu } from "mantine-contextmenu";
import Link from "next/link";
import { useEffect, useState } from "react";

import { SessionLinkRename } from "./session-link-rename";

export function SessionLink({ session }: { session: AiSessionListItem }) {
	const [shouldShow, setShouldShow] = useState(true); // for Optimistic UI

	const { replaceNewSession } = useAiNewSessionRouter();
	const { isCurrentSession } = useAiIsCurrentSession(session.session_id);
	const { hovered, ref } = useHover<HTMLAnchorElement>();
	const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

	const utils = api.useUtils();
	const deleteSession = api.ai.sessions.delete.useMutation({
		onError() {
			setShouldShow(true);
		},
		async onMutate() {
			await utils.ai.sessions.recents.cancel({});
			await utils.ai.sessions.favorites.cancel();
			setShouldShow(false);
		},
		async onSettled() {
			await utils.ai.sessions.invalidate();
			if (isCurrentSession) {
				replaceNewSession();
			}
		},
	});

	useEffect(() => {
		if (!hovered) {
			setShowDeleteConfirmation(false);
		}
	}, [hovered]);

	const { sessionTitle } = useAiSessionTitle({ sessionId: session.session_id });

	const [showRename, setShowRename] = useState(false);
	const [updatedTitle, setUpdatedTitle] = useState<string>(""); // for Optimistic UI

	const title = updatedTitle
		? updatedTitle
		: isCurrentSession
			? session.title ?? sessionTitle ?? session.session_id
			: session.title ?? session.session_id;

	const handleTitleChange = (newTitle: string) => {
		if (newTitle !== title) {
			setUpdatedTitle(newTitle);
		}
		setShowRename(false);
	};

	const { showContextMenu } = useContextMenu();
	const showMenu = showContextMenu([
		{
			icon: <IconTrash size="1rem" />,
			key: "delete",
			onClick: () => {
				deleteSession.mutate({
					sessionId: session.session_id,
				});
			},
			title: "Delete",
		},
		{
			icon: <IconPencil size="1rem" />,
			key: "rename",
			onClick: () => {
				setShowRename(true);
			},
			title: "Rename",
		},
		{ key: "divider" },
		{
			icon: <IconLink size="1rem" />,
			key: "copy-link",
			onClick: () => {
				navigator.clipboard.writeText(
					`${window.location.origin}/app/sessions/${session.session_id}`
				);
			},
			title: "Copy link",
		},
	]);

	return (
		<AnimatePresence>
			{shouldShow && (
				<m.div
					animate={{ height: "auto", scaleY: 1 }}
					exit={{ height: 0, opacity: 0, scaleY: 0, x: -100 }}
				>
					<Popover
						offset={0}
						onChange={setShowRename}
						opened={showRename}
						position="bottom"
						trapFocus
						width="target"
						withinPortal
					>
						<PopoverTarget>
							<NavLink
								active={isCurrentSession}
								component={Link}
								href={`/app/sessions/${session.session_id}`}
								key={session.session_id}
								label={
									<Tooltip label={title} openDelay={1000} position="bottom">
										<Text lineClamp={1}>{title}</Text>
									</Tooltip>
								}
								leftSection={<IconMessageCircle size="1.25rem" />}
								onContextMenu={showMenu}
								ref={ref}
								rightSection={
									<AnimatePresence>
										{hovered && (
											<m.span
												animate={{ opacity: 1 }}
												exit={{ opacity: 0 }}
												initial={{ opacity: 0 }}
												transition={{ duration: 0.08 }}
											>
												<Group gap="xs">
													<Tooltip
														label={"Rename, share, and more..."}
														position="bottom"
													>
														<ActionIcon
															color="gray"
															onClick={(e) => {
																e.preventDefault();
																e.stopPropagation();
																showMenu(e);
															}}
															size="1rem"
															variant="subtle"
														>
															<IconDots size="1rem" />
														</ActionIcon>
													</Tooltip>
													<Tooltip
														label={
															showDeleteConfirmation ? "Confirm" : "Delete"
														}
														position="bottom"
													>
														<ActionIcon
															color="red"
															onClick={(e) => {
																e.preventDefault();
																e.stopPropagation();
																if (showDeleteConfirmation) {
																	deleteSession.mutate({
																		sessionId: session.session_id,
																	});
																} else {
																	setShowDeleteConfirmation(true);
																}
															}}
															size="1rem"
															variant="subtle"
														>
															{showDeleteConfirmation ? (
																<IconCheck size="1rem" />
															) : (
																<IconTrash size="1rem" />
															)}
														</ActionIcon>
													</Tooltip>
												</Group>
											</m.span>
										)}
									</AnimatePresence>
								}
							/>
						</PopoverTarget>
						<PopoverDropdown p="0">
							<SessionLinkRename
								defaultTitle={title}
								onSubmit={handleTitleChange}
								session={session}
							/>
						</PopoverDropdown>
					</Popover>
				</m.div>
			)}
		</AnimatePresence>
	);
}

export function SessionLinkSkeleton() {
	return (
		<NavLink
			active={false}
			label={
				<Skeleton w="full">
					<Text>loading</Text>
				</Skeleton>
			}
		/>
	);
}
