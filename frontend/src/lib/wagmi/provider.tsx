"use client";

import { WagmiProvider as WagmiProvider_ } from "wagmi";

import { config } from "./config";

/**
 * Should be placed outside tanstack query provider
 */
export function WagmiProvider({ children }: { children: React.ReactNode }) {
	return <WagmiProvider_ config={config}>{children}</WagmiProvider_>;
}
