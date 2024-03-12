import { createTRPCRouter } from "@/lib/trpc/server";

import { executorApi } from "./executor";
import { executorCreateApi } from "./executor-create";
import { executorsApi } from "./executors";

export const executorRouter = createTRPCRouter({
	executor: executorApi,
	executorCreate: executorCreateApi,
	executors: executorsApi,
});
