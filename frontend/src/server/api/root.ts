import { createTRPCRouter } from "@/lib/trpc/server";

import { aiRouter } from "./routers/ai";
import { userSettingsRouter } from "./routers/user-settings";
import { executorRouter } from "./routers/executor";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
	ai: aiRouter,
	userSettings: userSettingsRouter,
	executor: executorRouter,
});
