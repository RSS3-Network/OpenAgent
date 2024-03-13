// https://env.t3.gg/docs/nextjs

import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
	client: {
		// NEXT_PUBLIC_PUBLISHABLE_KEY: z.string().min(1),
	},
	experimental__runtimeEnv: {
		// NEXT_PUBLIC_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_PUBLISHABLE_KEY,
	},
	server: {
		API_AI_URL: z.string().url(),
		API_EXECUTOR_URL: z.string().url(),
		AUTH_DISCORD_CLIENT_ID: z.string().min(1),
		AUTH_DISCORD_CLIENT_SECRET: z.string().min(1),
		AUTH_GMAIL_PASS: z.string().min(1),
		AUTH_GMAIL_USER: z.string().min(1),
		AUTH_GOOGLE_CLIENT_ID: z.string().min(1),
		AUTH_GOOGLE_CLIENT_SECRET: z.string().min(1),
		DATABASE_URL: z.string().url(),
		NEXTAUTH_URL: z.string().url(),
		NODE_ENV: z
			.enum(["development", "test", "production"])
			.default("development"),
	},
});
