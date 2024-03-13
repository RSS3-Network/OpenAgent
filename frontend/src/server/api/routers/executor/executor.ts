import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { minValue, number, object } from "valibot";

import { pool } from "./pool";

export const executorApi = protectedProcedure
	.input(
		wrap(
			object({
				executorId: number([minValue(1)]),
			})
		)
	)
	.query(async ({ ctx, input }) => {
		const userId = ctx.session?.user.id;
		const { executorId } = input;

		const res = await pool
			.request({
				method: "GET",
				path: `/executors/${userId}/${executorId}`,
			})
			.then(async (res) => {
				const result = (await res.body.json()) as any;
				return result?.data?.items?.[0] as Promise<ExecutorDetail>;
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
