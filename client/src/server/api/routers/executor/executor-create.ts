import { protectedProcedure } from "@/lib/trpc/server";
import { TRPCError } from "@trpc/server";

import { pool } from "./pool";

export const executorCreateApi = protectedProcedure.mutation(
	async ({ ctx }) => {
		const userId = ctx.session?.user.id;

		const res = await pool
			.request({
				body: JSON.stringify({
					userId,
				}),
				headers: {
					"Content-Type": "application/json",
				},
				method: "POST",
				path: `/executors`,
			})
			.then((res) => res.body.json() as Promise<ExecutorListItem>)
			.catch((err) => {
				console.error(err);
				throw new TRPCError({
					cause: err,
					code: "INTERNAL_SERVER_ERROR",
					message: "Internal Server Error",
				});
			});

		return res;
	}
);
