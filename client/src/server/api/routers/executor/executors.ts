import { protectedProcedure } from "@/lib/trpc/server";
import { TRPCError } from "@trpc/server";

import { pool } from "./pool";

export const executorsApi = protectedProcedure.query(async ({ ctx }) => {
	const userId = ctx.session?.user.id;

	const res = await pool
		.request({
			method: "GET",
			path: `/executors/${userId}`,
		})
		.then(async (res) => {
			const result = (await res.body.json()) as any;
			return result?.data?.items as Promise<ExecutorDetail[]>;
		})
		.catch((err) => {
			console.error(err);
			throw new TRPCError({
				cause: err,
				code: "INTERNAL_SERVER_ERROR",
				message: "Internal Server Error",
			});
		});

	return res;
});
