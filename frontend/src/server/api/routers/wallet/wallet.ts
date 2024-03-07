import { protectedProcedure } from "@/lib/trpc/server";
import { wrap } from "@/lib/validations/wrap";
import { TRPCError } from "@trpc/server";
import { minValue, number, object } from "valibot";

import { pool } from "./pool";

export const walletApi = protectedProcedure
	.input(
		wrap(
			object({
				walletId: number([minValue(1)]),
			})
		)
	)
	.query(async ({ ctx, input }) => {
		const userId = ctx.session?.user.id;
		const { walletId } = input;

		const res = await pool
			.request({
				method: "GET",
				path: `/wallets/${userId}/${walletId}`,
			})
			.then(async (res) => {
				const result = (await res.body.json()) as any;
				return result?.data?.items?.[0] as Promise<WalletDetail>;
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
