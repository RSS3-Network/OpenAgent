import { createTRPCRouter } from "@/lib/trpc/server";

import { aiRouter } from "./routers/ai";
import { executorRouter } from "./routers/executor";
import { userSettingsRouter } from "./routers/user-settings";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
	ai: aiRouter,
	executor: executorRouter,
	userSettings: userSettingsRouter,
});
