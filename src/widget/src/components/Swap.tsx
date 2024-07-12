/* eslint-disable no-console */
import { LiFiWidget } from '@lifi/widget';

function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    fromAmount: params.get('fromAmount') || 11,
    fromChain: params.get('fromChain') || 1,
    fromToken: params.get('fromToken') || 'eth',
    toChain: params.get('toChain') || 1,
    toToken: params.get('toToken') || 'weth',
  };
}

export function Swap() {
  const { fromAmount, fromChain, fromToken, toChain, toToken } = getQueryParams();

  return (
    <LiFiWidget
      integrator="vite-example"
      config={{
        fromAmount: Number(fromAmount),
        fromChain: Number(fromChain),
        fromToken,
        toChain: Number(toChain),
        toToken,
        theme: {
          container: {
            border: `1px solid rgb(234, 234, 234)`,
            borderRadius: '16px',
          },
        },
      }}
    />
  );
}
