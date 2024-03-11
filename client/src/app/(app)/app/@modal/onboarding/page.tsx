import { api } from "@/lib/trpc/server";
import { redirect } from "next/navigation";

import { OnboardingModal } from "./_component/onboarding-modal";

export default async function Page() {
	// check if the user has already completed the onboarding
	// if yes, redirect to the dashboard
	const wallets = await api.wallet.wallets.query();

	if (wallets.length > 0) {
		redirect("/app");
	}

	return <OnboardingModal />;
}
