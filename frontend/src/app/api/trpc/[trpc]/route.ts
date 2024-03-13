import { env } from "@/env.mjs";
import { createTRPCContext } from "@/lib/trpc/context";
import { appRouter } from "@/server/api/root";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { type NextRequest } from "next/server";

const handler = (req: NextRequest) =>
	fetchRequestHandler({
		createContext: () => createTRPCContext({ req }),
		endpoint: "/api/trpc",
		onError:
			env.NODE_ENV === "development"
				? ({ error, path }) => {
						console.error(
							`❌ tRPC failed on ${path ?? "<no-path>"}: ${error.message}`
						);
				  }
				: undefined,
		req,
		router: appRouter,
	});

export { handler as GET, handler as POST };
