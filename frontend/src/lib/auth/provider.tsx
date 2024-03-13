"use client";

import { SessionProvider as SessionProvider_ } from "next-auth/react";
import { type PropsWithChildren } from "react";

export function SessionProvider({ children }: PropsWithChildren<{}>) {
	return <SessionProvider_>{children}</SessionProvider_>;
}
