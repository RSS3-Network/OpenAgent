import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { WagmiProvider, createConfig, http } from 'wagmi';
import { base, mainnet } from 'wagmi/chains';
import { injected, safe, walletConnect } from 'wagmi/connectors';
import { App } from './App';
import {Route, BrowserRouter as Router, Routes} from "react-router-dom";
import {Swap} from "./components/Swap";

const queryClient = new QueryClient();

const projectId = import.meta.env.VITE_WALLET_CONNECT_PROJECT_ID;
console.log(projectId)
const config = createConfig({
  chains: [mainnet],
  connectors: [injected(), walletConnect({ projectId }), safe()],
  transports: {
    [mainnet.id]: http(),
    [base.id]: http(),
  },
});

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <WagmiProvider config={config}>
         <Router>

        <Routes>
          <Route path="/" element={<App  />} />
          <Route path="/swap/*" element={<Swap  />} />
        </Routes>
      </Router>


      </WagmiProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);
