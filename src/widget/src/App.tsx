import React from 'react';
import '@rainbow-me/rainbowkit/styles.css';
import { RainbowKitProvider, getDefaultConfig } from '@rainbow-me/rainbowkit';
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { mainnet, polygon, optimism, arbitrum } from 'wagmi/chains';

const config = getDefaultConfig({
  appName: 'My RainbowKit App',
  projectId: 'YOUR_PROJECT_ID', // Replace with your actual WalletConnect project ID
    chains: [mainnet, polygon, optimism, arbitrum],
  ssr: true,
});

const queryClient = new QueryClient();

export function App() {
  return (
    <div>
      <h1>Hello World</h1>
    </div>
  );
}

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
