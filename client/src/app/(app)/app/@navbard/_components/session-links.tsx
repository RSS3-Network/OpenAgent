"use client";

import { api } from "@/lib/trpc/client";

import { SessionLink, SessionLinkSkeleton } from "./session-link";

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

	return flattenedRecents.map((session) => (
		<SessionLink key={session.session_id} session={session} />
	));
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
