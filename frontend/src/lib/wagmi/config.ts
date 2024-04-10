import type { Transport } from "viem";
import type { Config } from "wagmi";

import { env } from "@/env.mjs";
import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import {
	arbitrum,
	bsc,
	mainnet,
	optimism,
	polygon,
	sepolia,
} from "wagmi/chains";

declare module "wagmi" {
	interface Register {
		config: Config<
			typeof chains,
			Record<(typeof chains)[number]["id"], Transport>
		>;
	}
}

const chains = [mainnet, sepolia, optimism, polygon, arbitrum, bsc] as const;

export const config = getDefaultConfig({
	appName: "OpenAgent",
	chains,
	projectId: env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID,
	ssr: true, // If your dApp uses server side rendering (SSR)
});

export const chainId = env.NEXT_PUBLIC_CHAIN_ID;
