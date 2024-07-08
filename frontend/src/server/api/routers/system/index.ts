import { createTRPCRouter } from "@/lib/trpc/server";

import { authProvidersApi } from "./settings";

export const systemRouter = createTRPCRouter({
	authProviders: authProvidersApi,
});
