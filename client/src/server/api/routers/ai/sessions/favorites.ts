import { protectedProcedure } from "@/lib/trpc/server";
import { TRPCError } from "@trpc/server";

import { pool } from "../pool";

export const favoriteSessionsApi = protectedProcedure.query(async ({ ctx }) => {
	const user_id = ctx.session?.user.id;

	const result = await pool
		.request({
			method: "GET",
			path: "/sessions/tab/favorites",
			query: {
				user_id: user_id ?? "",
			},
		})
		.then(async (res) => {
			return res.body.json() as Promise<AiSessionTree>;
		})
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
