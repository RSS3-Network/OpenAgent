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
		AUTH_DISCORD_CLIENT_ID: z.string().min(1),
		AUTH_DISCORD_CLIENT_SECRET: z.string().min(1),
		AUTH_GMAIL_PASS: z.string().min(1),
		AUTH_GMAIL_USER: z.string().min(1),
		AUTH_GOOGLE_CLIENT_ID: z.string().min(1),
		AUTH_GOOGLE_CLIENT_SECRET: z.string().min(1),
		BACKEND_URL: z.string().url(),
		NEXTAUTH_URL: z.string().url(),
		NODE_ENV: z
			.enum(["development", "test", "production"])
			.default("development"),
		POSTGRES_DATABASE_URL: z.string().url(),
	},
});
