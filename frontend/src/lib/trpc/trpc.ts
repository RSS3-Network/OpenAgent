import { initTRPC } from "@trpc/server";
import superjson from "superjson";
import { ValiError, flatten } from "valibot";

import { createTRPCContext } from "./context";

/**
 * INITIALIZATION
 *
 * This is where the tRPC API is initialized, connecting the context and transformer. We also parse
 * ValiErrors so that you get typesafety on the frontend if your procedure fails due to validation
 * errors on the backend.
 */
export const t = initTRPC.context<typeof createTRPCContext>().create({
	errorFormatter({ error, shape }) {
		if (error.cause instanceof ValiError) {
			return {
				...shape,
				data: {
					...shape.data,
					valiError: flatten(error.cause),
				},
			};
		}

		return {
			...shape,
			data: {
				...shape.data,
				valiError: null,
			},
		};
	},
	transformer: superjson,
});
