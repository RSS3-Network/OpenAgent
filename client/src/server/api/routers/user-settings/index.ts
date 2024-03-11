import { createTRPCRouter } from "@/lib/trpc/server";

import { settingsApi } from "./settings";

export const userSettingsRouter = createTRPCRouter({
	settings: settingsApi,
});
