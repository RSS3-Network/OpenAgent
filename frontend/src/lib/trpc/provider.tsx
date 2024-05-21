"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { loggerLink, unstable_httpBatchStreamLink } from "@trpc/client";
import { useState } from "react";

import { api } from "./client";
import { getUrl, transformer } from "./shared";

export function TrpcProvider(props: {
	children: React.ReactNode;
	headers: Headers;
}) {
	const [queryClient] = useState(() => new QueryClient());

	const [trpcClient] = useState(() =>
		api.createClient({
			links: [
				loggerLink({
					enabled: (op) =>
						process.env.NODE_ENV === "development" ||
						(op.direction === "down" && op.result instanceof Error),
				}),
				unstable_httpBatchStreamLink({
					headers() {
						const heads = new Map(props.headers);
						heads.set("x-trpc-source", "react");
						return Object.fromEntries(heads);
					},
					transformer,
					url: getUrl(),
				}),
			],
		})
	);

	return (
		<QueryClientProvider client={queryClient}>
			<api.Provider client={trpcClient} queryClient={queryClient}>
				{props.children}
				<ReactQueryDevtools
					buttonPosition="bottom-left"
					initialIsOpen={false}
				/>
			</api.Provider>
		</QueryClientProvider>
	);
}
