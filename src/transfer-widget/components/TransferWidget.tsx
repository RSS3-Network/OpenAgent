import React, { useState, useEffect } from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import {
  useSendTransaction,
  useWaitForTransactionReceipt,
  useAccount,
  useBalance,
  useConfig,
  type BaseError
} from 'wagmi';
import { parseUnits } from 'viem';
import styles from '../styles/TransferWidget.module.css';

interface TransferWidgetProps {
  token: string;
  amount: string;
  toAddress: string;
  chainName: string;
}

const TransferWidget: React.FC<TransferWidgetProps> = ({
  token,
  amount,
  toAddress,
  chainName
}) => {
  const [currentAmount, setCurrentAmount] = useState(amount);
  const [currentToAddress, setCurrentToAddress] = useState(toAddress);
  const [account, setAccount] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('');
  const { address } = useAccount();
  const config = useConfig();
  const { data: balance } = useBalance({ address, token: token as `0x${string}` });

  const {
    data: hash,
    error,
    isPending,
    sendTransaction
  } = useSendTransaction();

  const {
    isLoading: isConfirming,
    isSuccess: isConfirmed
  } = useWaitForTransactionReceipt({ hash });

  useEffect(() => {
    if (address) {
      setAccount(address);
    }

  }, [address]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (account) {
      sendTransaction({
        to: toAddress as `0x${string}`,
        value: parseUnits(amount, balance?.decimals || 18),
      });
    } else {
      setStatus('Wallet is not connected');
    }
  };

  return (
    <div className={styles.transferWidget}>
      <h3>Send</h3>
      <div className={styles.accountInfo}>
        <p>Account 1</p>
        <p>{account || 'Not connected'}</p>
      </div>
      <div className={styles.assetInfo}>
        <label>Asset:</label>
        <div className={styles.assetDetails}>
          <span>{token}</span>
          <span className={styles.balance}>Balance: {balance?.formatted || 0} {token}</span>
        </div>
      </div>
      <div className={styles.amountInfo}>
        <label>Amount:</label>
        <input
          type="text"
          value={amount}
          onChange={(e) => setCurrentAmount(e.target.value)}
          placeholder="Enter amount"
        />
      </div>
      <div className={styles.addressInfo}>
        <label>To Address:</label>
        <input
          type="text"
          value={toAddress}
          onChange={(e) => setCurrentToAddress(e.target.value)}
          placeholder="Enter recipient address"
        />
      </div>
      <div className={styles.gasFeeInfo}>
        <p>Estimated gas fee</p>
        <p>0 Gwei</p>
        <p>Max fee: 0 ETH</p>
      </div>
      <div className={styles.buttonGroup}>
        <ConnectButton />
        <button className={styles.transferButton} onClick={handleSubmit} disabled={!account || isPending || isConfirming}>
          {isPending ? 'Confirming...' : isConfirming ? 'Processing...' : 'Send'}
        </button>
      </div>
      <div className={styles.status}>{status}</div>
      {hash && <div className={styles.transactionInfo}>Transaction Hash: {hash}</div>}
      {isConfirming && <div className={styles.transactionInfo}>Waiting for confirmation...</div>}
      {isConfirmed && <div className={styles.transactionInfo}>Transaction confirmed.</div>}
      {error && (
        <div className={styles.error}>Error: {(error as BaseError).shortMessage || error.message}</div>
      )}
    </div>
  );
};

export default TransferWidget;
