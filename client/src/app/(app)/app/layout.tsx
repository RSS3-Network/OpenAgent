import { Spotlight } from "@/components/spotlight";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { type ReactNode } from "react";

import { AppLayout } from "./_components/layout";

export default async function Layout({
	children,
	headerl,
	headerr,
	modal,
	navbard,
	navbart,
}: {
	children: ReactNode;
	headerl: ReactNode;
	headerr: ReactNode;
	modal: ReactNode;
	navbard: ReactNode;
	navbart: ReactNode;
}) {
	const session = await auth();
	if (!session?.user.id) {
		redirect("/login");
	}

	return (
		<AppLayout
			headerl={headerl}
			headerr={headerr}
			modal={modal}
			navbard={navbard}
			navbart={navbart}
		>
			{children}
			<Spotlight />
		</AppLayout>
	);
}
