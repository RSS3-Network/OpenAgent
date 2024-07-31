import React, { useState } from 'react';
import { useAccount, useConnect, useDisconnect, useNetwork, useSwitchNetwork, useBalance, useSendTransaction } from 'wagmi';
import { InjectedConnector } from 'wagmi/connectors/injected';
import { parseEther } from 'ethers/lib/utils';
import { Box, Button, Typography, Paper, CircularProgress } from '@mui/material';

interface TransferWidgetProps {
  to_address: string;
  token: string;
  token_address: string;
  amount: string;
  chain_name: string;
  chain_id: number;
  logo_uri: string;
}

export const TransferWidget: React.FC<TransferWidgetProps> = (props) => {
  const [isTransferring, setIsTransferring] = useState(false);
  const { address, isConnected } = useAccount();
  const { connect } = useConnect({
    connector: new InjectedConnector(),
  });
  const { disconnect } = useDisconnect();
  const { chain } = useNetwork();
  const { switchNetwork } = useSwitchNetwork();
  const { data: balance } = useBalance({ address });
  const { sendTransaction } = useSendTransaction();

  // @ts-ignore
  const handleConnect = async () => {
    await connect();
  };

  // @ts-ignore
  const handleTransfer = async () => {
    if (!isConnected) return;

    setIsTransferring(true);
    try {
      if (chain?.id !== props.chain_id) {
        await switchNetwork?.(props.chain_id);
      }

      await sendTransaction({
        to: props.to_address,
        value: parseEther(props.amount),
      });

      // You might want to add some success feedback here
    } catch (error) {
      console.error('Transfer failed:', error);
      // You might want to add some error feedback here
    } finally {
      setIsTransferring(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 400, margin: 'auto' }}>
      <Typography variant="h5" gutterBottom align="center">
        Crypto Transfer
      </Typography>
      <Box sx={{ mb: 2 }}>
        <Typography variant="body1">
          Amount: {props.amount} {props.token}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          on {props.chain_name}
        </Typography>
      </Box>
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="textSecondary">To</Typography>
        <Typography variant="body1" sx={{ wordBreak: 'break-all' }}>
          {props.to_address}
        </Typography>
      </Box>
      {isConnected ? (
        <>
          <Typography variant="body2" sx={{ mb: 1 }}>
            Connected: {address}
          </Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>
            Balance: {balance?.formatted} {balance?.symbol}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleTransfer}
            disabled={isTransferring}
          >
            {isTransferring ? <CircularProgress size={24} /> : 'Confirm Transfer'}
          </Button>
          <Button
            variant="outlined"
            color="secondary"
            fullWidth
            onClick={() => disconnect()}
            sx={{ mt: 1 }}
          >
            Disconnect
          </Button>
        </>
      ) : (
        <Button
          variant="contained"
          color="primary"
          fullWidth
          onClick={handleConnect}
        >
          Connect Wallet
        </Button>
      )}
    </Paper>
  );
};