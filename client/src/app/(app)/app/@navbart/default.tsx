import { auth } from "@/lib/auth";

import { NavLinksSystem } from "./_components/nav-links-system";
import { UserMenu } from "./_components/user-menu";

export default async function Page() {
	const session = await auth();

	if (!session?.user.id) {
		return null;
	}

	return (
		<div>
			<UserMenu
				email={session.user.email}
				image={session.user.image}
				username={session.user.name}
			/>
			<NavLinksSystem />
		</div>
	);
}
