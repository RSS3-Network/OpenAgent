import type { Transport } from "viem";

import { env } from "@/env.mjs";
import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { Config, Register } from "wagmi";
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

declare global {
	// Used to convert string chain IDs to their number equivalents
	// e.g. const n = Number("42") // n's type is `42` instead of `number`
	interface NumberConstructor {
		<T extends string>(value: T): T extends `${infer N extends number}`
			? N
			: number;
	}
}

export type ValidChainId = Register["config"]["chains"][number]["id"];

const chains = [mainnet, sepolia, optimism, polygon, arbitrum, bsc] as const;

export const config = getDefaultConfig({
	appName: "OpenAgent",
	chains,
	projectId: env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID,
	ssr: true, // If your dApp uses server side rendering (SSR)
});

export const chainId = env.NEXT_PUBLIC_CHAIN_ID as ValidChainId;
