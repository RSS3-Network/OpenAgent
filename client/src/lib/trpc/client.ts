import { createTRPCReact } from "@trpc/react-query";
// import {
// 	experimental_createActionHook,
// 	experimental_createTRPCNextAppDirClient,
// 	experimental_serverActionLink,
// } from "@trpc/next/app-dir/client";
// import { experimental_nextHttpLink } from "@trpc/next/app-dir/links/nextHttp";
import { type AppRouter } from "./shared";

export const api = createTRPCReact<AppRouter>();

// https://github.com/trpc/trpc/blob/66c8000db3dbb1fe193f59a69708e8964492f134/examples/.experimental/next-app-dir/src/trpc/client.ts
// export const experimental_api = experimental_createTRPCNextAppDirClient<AppRouter>({
// 	config() {
// 		return {
// 			transformer: superjson,
// 			links: [
// 				loggerLink({
// 					enabled: (op) => true,
// 				}),
// 				experimental_nextHttpLink({
// 					batch: true,
// 					url: getUrl(),
// 					headers() {
// 						return {
// 							"x-trpc-source": "client",
// 						};
// 					},
// 				}),
// 			],
// 		};
// 	},
// });

// export const useAction = experimental_createActionHook({
// 	links: [loggerLink(), experimental_serverActionLink()],
// 	transformer: superjson,
// });
