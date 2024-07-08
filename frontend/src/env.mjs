// https://env.t3.gg/docs/nextjs

import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
	client: {
		NEXT_PUBLIC_CHAIN_ID: z.coerce.number().min(1),
		NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID: z.string().min(1),
	},
	experimental__runtimeEnv: {
		NEXT_PUBLIC_CHAIN_ID: process.env.NEXT_PUBLIC_CHAIN_ID,
		NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID:
			process.env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID,
	},
	server: {
		API_EXECUTOR_URL: z.string().url(),
		AUTH_DISCORD_CLIENT_ID: z.string().optional(),
		AUTH_DISCORD_CLIENT_SECRET: z.string().optional(),
		AUTH_GMAIL_PASS: z.string().optional(),
		AUTH_GMAIL_USER: z.string().optional(),
		AUTH_GOOGLE_CLIENT_ID: z.string().optional(),
		AUTH_GOOGLE_CLIENT_SECRET: z.string().optional(),
		BACKEND_URL: z.string().url(),
		NEXTAUTH_URL: z.string().url(),
		NODE_ENV: z
			.enum(["development", "test", "production"])
			.default("development"),
		POSTGRES_DATABASE_URL: z.string().url(),
	},
});

// at least one AUTH_* env var must be set
if (
	!env.server.AUTH_DISCORD_CLIENT_ID &&
	!env.server.AUTH_GMAIL_PASS &&
	!env.server.AUTH_GOOGLE_CLIENT_ID
) {
	throw new Error(
		"At least one AUTH_* env var must be set so users can log in"
	);
}
