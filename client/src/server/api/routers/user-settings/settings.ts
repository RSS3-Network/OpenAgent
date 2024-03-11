import { protectedProcedure } from "@/lib/trpc/server";

export const settingsApi = protectedProcedure.query(async ({ ctx, input }) => {
	const user_id = ctx.session.user.id;

	await ctx.db.userSettings.findUnique({
		where: {
			userId: user_id,
		},
	});

	return {};
});
