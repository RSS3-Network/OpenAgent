import React from 'react';
import '@rainbow-me/rainbowkit/styles.css';
import {RainbowKitProvider, getDefaultConfig, getDefaultWallets} from '@rainbow-me/rainbowkit';
import {createConfig, http, WagmiProvider} from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import {mainnet, sepolia} from 'wagmi/chains';

let MAINNET_RPC_URL = process.env.REACT_APP_MAINNET_RPC_URL || "";
let SEPOLIA_RPC_URL = process.env.REACT_APP_SEPOLIA_RPC_URL || "";

/* eslint-disable no-console */
export function App() {
  return <>
  </>
}

const { connectors } = getDefaultWallets({
  appName: "OpenAgent Widget",
  appDescription: "Widget",
  projectId: "project id",
})

export const wagmiConfig = createConfig({
  chains:[mainnet,sepolia],
  connectors,
  ssr: true,
  transports: {
    [mainnet.id]: http(MAINNET_RPC_URL, { batch: true }),
    [sepolia.id]: http(SEPOLIA_RPC_URL, { batch: true }),
  },
  syncConnectedChain: true,
})

declare module "wagmi" {
  interface Register {
    config: typeof wagmiConfig
  }
}

// Create a new QueryClient instance for React Query
const queryClient = new QueryClient();

/**
 * TransferWidgetApp component.
 * Wraps children with necessary providers for Wagmi, React Query, and RainbowKit.
 *
 * @param {Object} props - The component props
 * @param {React.ReactNode} props.children - The child components to be wrapped
 */
export function TransferWidgetApp({ children }: { children: React.ReactNode }) {
  return (
      <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>
          {children}
       </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
