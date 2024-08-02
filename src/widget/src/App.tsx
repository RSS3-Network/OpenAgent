import React from 'react';
import '@rainbow-me/rainbowkit/styles.css';
import { RainbowKitProvider, getDefaultConfig } from '@rainbow-me/rainbowkit';
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { mainnet, polygon, optimism, arbitrum } from 'wagmi/chains';

/* eslint-disable no-console */

export function App() {

  return <>
  <h1>hello world</h1>
  </>
}

// Configuration for RainbowKit
const config = getDefaultConfig({
  appName: 'My RainbowKit App',
  projectId: 'No_ID',
    chains: [mainnet, polygon, optimism, arbitrum],
  ssr: true,
});

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
      <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>
          {children}
       </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
