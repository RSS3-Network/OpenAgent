import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { number, object, string, uuid } from "valibot";

import { pool } from "../pool";

export const cancelApi = protectedProcedure
	.input(
		wrap(
			object({
				taskId: string([uuid()]),
			})
		)
	)
	.mutation(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				body: JSON.stringify({
					task_id: input.taskId,
					user_id: user_id,
				}),
				method: "POST",
				path: `/tasks/cancel_task`,
			})
			.then(async (res) => {
				if (res.statusCode === 200) {
					return res.body.json() as Promise<string>;
				}

				const error = (await res.body.json()) as AiGeneralError;
				throw new Error(error.message, { cause: error });
			})
			.catch((err) => {
				throw new TRPCError({
					cause: err,
					code: "INTERNAL_SERVER_ERROR",
					message: err.message || "Internal Server Error",
				});
			});

		return {
			result,
		};
	});
