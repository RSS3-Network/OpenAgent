import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import {
	maxValue,
	minValue,
	number,
	object,
	optional,
	picklist,
	string,
	uuid,
} from "valibot";

import { pool } from "../pool";

export const allApi = protectedProcedure
	.input(
		wrap(
			object({
				cursor: optional(number(), 0),
				limit: optional(number([minValue(1), maxValue(100)]), 50),
				sessionId: optional(string([uuid()])),
				status: optional(
					picklist(["idle", "pending", "running", "done", "canceled", "failed"])
				),
			})
		)
	)
	.query(async ({ ctx, input }) => {
		const user_id = ctx.session?.user.id;

		const { sessionId, status } = input;

		const result = await pool
			.request({
				method: "GET",
				path: "/tasks/query_list",
				query: {
					...(sessionId && { session_id: sessionId }),
					...(status && { status: status }),
					user_id: user_id,
				},
			})
			.then(async (res) => {
				return res.body.json() as Promise<AiTaskItemList>;
			})
			.catch((err) => {
				throw new TRPCError({
					cause: err,
					code: "INTERNAL_SERVER_ERROR",
					message: "Internal Server Error",
				});
			});

		return {
			nextCursor: result.length > 0 ? input.cursor + input.limit : null,
			result,
		};
	});
