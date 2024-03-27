import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { number, object, string, uuid } from "valibot";

import { pool } from "../../pool";

export const transferApi = protectedProcedure
	.input(
		wrap(
			object({
				amount: string(),
				executorId: number(),
				taskId: string([uuid()]),
				toAddress: string([]),
				tokenAddress: string([]),
			})
		)
	)
	.mutation(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				body: JSON.stringify({
					amount: input.amount,
					executor_id: input.executorId,
					task_id: input.taskId,
					to_address: input.toAddress,
					token_address: input.tokenAddress,
					user_id: user_id,
				}),
				method: "POST",
				path: `/tasks/confirm_transfer`,
			})
			.then(async (res) => {
				if (res.statusCode === 200) {
					return res.body.json() as Promise<AiTaskActionResponse_Transfer>;
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
