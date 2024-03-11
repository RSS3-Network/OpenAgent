import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { object, string, uuid } from "valibot";

import { pool } from "../pool";

export const deleteSessionApi = protectedProcedure
	.input(
		wrap(
			object({
				sessionId: string([uuid()]),
			})
		)
	)
	.mutation(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				method: "DELETE",
				path: `/sessions/${user_id}/${input.sessionId}`,
			})
			.then((res) => res.body.json() as Promise<string>)
			.catch((err) => {
				throw new TRPCError({
					cause: err,
					code: "INTERNAL_SERVER_ERROR",
					message: "Internal Server Error",
				});
			});

		return {
			result,
		};
	});
