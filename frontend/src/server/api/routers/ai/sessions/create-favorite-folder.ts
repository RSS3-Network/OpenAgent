import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { object, string, uuid } from "valibot";

import { pool } from "../pool";

export const createFavoriteFolderApi = protectedProcedure
	.input(
		wrap(
			object({
				order: string(),
				title: string(),
			})
		)
	)
	.mutation(async ({ ctx, input }) => {
		const user_id = ctx.session.user.id;

		const result = await pool
			.request({
				body: JSON.stringify({
					order: input.order,
					title: input.title,
					user_id: user_id,
				}),
				method: "POST",
				path: `/sessions/create_session_folder`,
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
