import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import {
	nullable,
	number,
	object,
	optional,
	picklist,
	string,
	uuid,
} from "valibot";

import { pool } from "../pool";

// {
//   "user_id": "jackma",
//   "session_id": "1234567890",
//   "title": "string",
//   "order": 0,
//   "tab": "favorite",
//   "parent_id": "string"
// }

export const updateSessionApi = protectedProcedure
	.input(
		wrap(
			object({
				order: optional(number()),
				parentId: optional(nullable(string([uuid()]))),
				sessionId: string([uuid()]),
				tab: optional(picklist(["favorite", "recent"])),
				title: optional(string()),
			})
		)
	)
	.mutation(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				body: JSON.stringify({
					order: 0,
					parent_id: input.parentId,
					session_id: input.sessionId,
					tab: input.tab,
					title: input.title,
					user_id: user_id,
				}),
				method: "PATCH",
				path: `/sessions/update_session`,
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
