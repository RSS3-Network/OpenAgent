import { api } from "@/lib/trpc/server";
import { type Metadata } from "next";
import { Suspense } from "react";

import { Messages, MessagesSkeleton } from "../../../../../components/messages";
import { MessageBox } from "../../_components/message-box";
import { NewSessionGuide } from "./_components/new-session-guide";
import { NewSessionGuideOnboarding } from "./_components/new-session-guide-onboarding";

type Props = {
	params: {
		id: string;
	};
	searchParams: {
		new?: "true";
		onboarding?: "true";
	};
};

export async function generateMetadata({
	params,
	searchParams,
}: Props): Promise<Metadata> {
	let title = "New Chat";
	if (searchParams.new !== "true") {
		const data = await api.ai.sessions.detail.query({
			limit: 1,
			sessionId: params.id,
		});
		title = data.result.title ?? params.id;
	}
	return {
		title,
	};
}

export default async function Page({ params, searchParams }: Props) {
	const sessionId = params.id;
	const isNewPage = searchParams.new === "true";
	const isOnboardingPage = searchParams.onboarding === "true";

	if (isOnboardingPage) {
		return (
			<>
				{isNewPage && <NewSessionGuideOnboarding sessionId={sessionId} />}

				<Suspense fallback={isNewPage ? null : <MessagesSkeleton />}>
					<Messages sessionId={sessionId} />
				</Suspense>
			</>
		);
	}

	return (
		<>
			{isNewPage && <NewSessionGuide sessionId={sessionId} />}

			<Suspense fallback={isNewPage ? null : <MessagesSkeleton />}>
				<Messages sessionId={sessionId} />
			</Suspense>

			<MessageBox sessionId={sessionId} />
		</>
	);
}
