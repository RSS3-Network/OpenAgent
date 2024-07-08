import { env } from "@/env.mjs";
import { publicProcedure } from "@/lib/trpc/server";

export const authProvidersApi = publicProcedure.query(async () => {
	return {
		providers: {
			discord: env.AUTH_DISCORD_CLIENT_ID,
			email: env.AUTH_GMAIL_USER,
			google: env.AUTH_GOOGLE_CLIENT_ID,
		},
	};
});
