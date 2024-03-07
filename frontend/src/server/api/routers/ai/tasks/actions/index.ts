import { createTRPCRouter } from "@/lib/trpc/server";

import { transferApi } from "./transfer";

export const actionsRouter = createTRPCRouter({
	transfer: transferApi,
});
