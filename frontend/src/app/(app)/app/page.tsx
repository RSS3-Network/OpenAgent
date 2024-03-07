import { getNewSessionHref, getOnboardingHref } from "@/lib/ai/utils";
import { api } from "@/lib/trpc/server";
import { redirect } from "next/navigation";

export default async function Page() {
	const session = await api.ai.sessions.recents.query({ limit: 1 });

	if (session.result.length > 0) {
		redirect(getNewSessionHref());
	} else {
		redirect(getOnboardingHref());
	}

	return <></>;
}
