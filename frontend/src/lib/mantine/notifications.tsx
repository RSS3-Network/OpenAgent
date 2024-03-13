import { Notifications } from "@mantine/notifications";
import "@mantine/notifications/styles.css";
import { PropsWithChildren } from "react";

export function NotificationsProvider({ children }: PropsWithChildren) {
	return (
		<>
			<Notifications />
			{children}
		</>
	);
}
