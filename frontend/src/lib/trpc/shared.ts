import { appRouter } from "@/server/api/root";
import { type inferRouterInputs, type inferRouterOutputs } from "@trpc/server";
import superjson from "superjson";

export const transformer = superjson;

function getBaseUrl() {
	if (typeof window !== "undefined") return "";
	const vc = process.env.VERCEL_URL;
	if (vc) return "https://" + vc;
	return "http://localhost:3000";
}

export function getUrl() {
	return getBaseUrl() + "/api/trpc";
}

export type AppRouter = typeof appRouter;

/**
 * Inference helper for inputs.
 *
 * @example type HelloInput = RouterInputs['example']['hello']
 */
export type RouterInputs = inferRouterInputs<AppRouter>;

/**
 * Inference helper for outputs.
 *
 * @example type HelloOutput = RouterOutputs['example']['hello']
 */
export type RouterOutputs = inferRouterOutputs<AppRouter>;
