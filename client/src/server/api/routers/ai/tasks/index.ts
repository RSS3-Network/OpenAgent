import { createTRPCRouter } from "@/lib/trpc/server";

import { actionsRouter } from "./actions";
import { allApi } from "./all";
import { cancelApi } from "./cancel";
import { detailApi } from "./detail";

export const tasksRouter = createTRPCRouter({
	actions: actionsRouter,
	all: allApi,
	cancel: cancelApi,
	detail: detailApi,
});
