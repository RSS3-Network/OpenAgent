import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { AiSessionErrorResponse } from "@/server/api/routers/ai/types/session";
import { TRPCError } from "@trpc/server";
import { object, string, uuid } from "valibot";

import { pool } from "../pool";

export const detailApi = protectedProcedure
	.input(
		wrap(
			object({
				taskId: string([uuid()]),
			})
		)
	)
	.query(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				method: "GET",
				path: `/tasks/fetch_one_task`,
				query: {
					task_id: input.taskId,
					user_id: user_id,
				},
			})
			.then(async (res) => {
				if (res.statusCode === 200) {
					return res.body.json() as Promise<AiTaskItem>;
				} else if (res.statusCode === 400) {
					const errorRes = (await res.body.json()) as AiSessionErrorResponse;
					if (errorRes.message === "task not found") {
						return null;
					}
				}
				console.log(res.statusCode);
				return null;
			})
			.catch(async (err) => {
				throw new TRPCError({
					cause: err,
					code: "INTERNAL_SERVER_ERROR",
					message: "Internal Server Error",
				});
			});

		return result;
	});
