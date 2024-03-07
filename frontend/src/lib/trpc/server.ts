import { loggerLink, unstable_httpBatchStreamLink } from "@trpc/client";
import { experimental_createServerActionHandler } from "@trpc/next/app-dir/server";
import { TRPCError } from "@trpc/server";
import { headers } from "next/headers";

import { createInnerTRPCContext } from "./context";
import { createTRPCJotai } from "./jotai";
import { type AppRouter, getUrl, transformer } from "./shared";
import { t } from "./trpc";

export const api = createTRPCJotai<AppRouter>({
	links: [
		loggerLink({
			enabled: (op) =>
				process.env.NODE_ENV === "development" ||
				(op.direction === "down" && op.result instanceof Error),
		}),
		unstable_httpBatchStreamLink({
			headers() {
				const heads = new Map(headers());
				heads.set("x-trpc-source", "rsc");
				return Object.fromEntries(heads);
			},
			url: getUrl(),
		}),
	],
	transformer,
});

/**
 * This is how you create new routers and sub-routers in your tRPC API.
 *
 * @see https://trpc.io/docs/router
 */
export const createTRPCRouter = t.router;

/**
 * Public (unauthenticated) procedure
 *
 * This is the base piece you use to build new queries and mutations on your tRPC API. It does not
 * guarantee that a user querying is authorized, but you can still access user session data if they
 * are logged in.
 */
export const publicProcedure = t.procedure;

/** Reusable middleware that enforces users are logged in before running the procedure. */
const enforceUserIsAuthed = t.middleware(({ ctx, next }) => {
	if (!ctx.session || !ctx.session.user) {
		throw new TRPCError({ code: "UNAUTHORIZED" });
	}
	return next({
		ctx: {
			// infers the `session` as non-nullable
			session: { ...ctx.session, user: ctx.session.user },
		},
	});
});

/**
 * Protected (authenticated) procedure
 *
 * If you want a query or mutation to ONLY be accessible to logged in users, use this. It verifies
 * the session is valid and guarantees `ctx.session.user` is not null.
 *
 * @see https://trpc.io/docs/procedures
 */
export const protectedProcedure = t.procedure.use(enforceUserIsAuthed);

/**
 * Experimental: Server Action Handler
 */
export const createAction = experimental_createServerActionHandler(t, {
	createContext() {
		return createInnerTRPCContext({
			headers: headers(),
		});
	},
});
