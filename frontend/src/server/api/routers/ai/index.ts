import { createTRPCRouter } from "@/lib/trpc/server";

import { sessionsRouter } from "./sessions";
import { tasksRouter } from "./tasks";

export const aiRouter = createTRPCRouter({
	sessions: sessionsRouter,
	tasks: tasksRouter,
});
