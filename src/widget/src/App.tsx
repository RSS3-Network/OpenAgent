/* eslint-disable no-console */

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

export function App() {

  return <>
  <h1>hello world</h1>
  </>
}
