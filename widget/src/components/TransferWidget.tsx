import React, {useState, useEffect} from 'react';
import {ConnectButton} from '@rainbow-me/rainbowkit';
import {
    useSendTransaction,
    useWaitForTransactionReceipt,
    useWriteContract,
    useAccount,
    useBalance,
    useEstimateGas,
    useFeeData,
    type BaseError, useEnsAddress
} from 'wagmi';
import {
    erc20Abi,
    encodeFunctionData,
    parseUnits,
    parseEther,
    formatEther,
    isAddress
} from 'viem';
import styles from './TransferWidget.module.css';

// Define the prop types for the TransferWidget component
interface TransferWidgetProps {
    token: string,
    amount: string,
    toAddress: string,
    tokenAddress?: string
}

/**
 * TransferWidgetComponent - A component for handling cryptocurrency token transfers.
 */
const TransferWidgetComponent: React.FC<TransferWidgetProps> = ({
            token,
            tokenAddress,
            amount,
            toAddress,
        }) => {
     // States for holding input values, account, and other dynamic data
    const [currentAmount, setCurrentAmount] = useState(amount);
    const [currentToAddress, setCurrentToAddress] = useState(toAddress);
    const [account, setAccount] = useState<string | null>(null);
    const [estimatedGasFee, setEstimatedGasFee] = useState<string>('0');
    const [estimationError, setEstimationError] = useState<string | null>(null);
    const [status, setStatus] = useState<string>('');
    const {address} = useAccount();
    const [isAmountValid, setIsAmountValid] = useState(true);

    const {
        data: hash1,
        error: error1,
        isPending: isPending1,
        sendTransaction
    } = useSendTransaction();

    const { writeContract, data: hash2, error: error2, isPending: isPending2 } = useWriteContract();

	const isErc20 = tokenAddress !== "0x0000000000000000000000000000000000000000";
    const hash = isErc20 ? hash2 : hash1;
	const error = isErc20 ? error2 : error1;
	const isPending = isErc20 ? isPending2 : isPending1;

    // Get the user wallet balance
    const {data: balance, isError: balanceError, isLoading: balanceLoading} = useBalance({
        address,
        token: !isErc20? undefined : tokenAddress as `0x${string}`,
    });
    const {
        isLoading: isConfirming,
        isSuccess: isConfirmed
    } = useWaitForTransactionReceipt({hash});


    // Estimate the gas required for the transaction
    const { data: estimatedGas, isError: isEstimateError } = useEstimateGas({
        to: currentToAddress as `0x${string}`,
        value: parseUnits(currentAmount || '0', balance?.decimals || 18),
        data: isErc20 ? encodeFunctionData({
            abi: erc20Abi,
            functionName: 'transfer',
            args: [currentToAddress as `0x${string}`, parseUnits(currentAmount || '0', balance?.decimals || 18)]
        }) : undefined,
    });

     // Resolve ENS name
    const { data: resolvedAddress, isLoading: isResolvingENS } = useEnsAddress({
        name: isAddress(currentToAddress) ? undefined : currentToAddress,
        chainId: 1,
    });

    // Feture the fee data
    const { data: feeData } = useFeeData();

    // Calculate gas fee
    useEffect(() => {
        // console.log("estimatedGas is:", estimatedGas);
        // console.log("feeData object is:", feeData);
        if (estimatedGas && feeData?.maxFeePerGas) {

            // Multiply estimated gas by maxFeePerGas to get the gas fee in Wei and then in Eth
            const gasFeeInWei = estimatedGas * feeData.maxFeePerGas;
            const gasFeeInEth = formatEther(gasFeeInWei);

            // console.log("Gas fee in ETH:", gasFeeInEth);
            setEstimatedGasFee(Number(gasFeeInEth).toFixed(8));
        } else {
            console.log("Missing estimatedGas or feeData.maxFeePerGas");
            setEstimatedGasFee('0.00000000');
        }
    }, [estimatedGas, feeData]);

    // Check if amount and gas fee is greater than balance
     useEffect(() => {

        //  console.log("Balance:", balance);
        // console.log("Current Amount:", currentAmount);
        // console.log("Estimated Gas Fee:", estimatedGasFee);
        if (balance && currentAmount && estimatedGasFee) {

            const amountWei = parseUnits(currentAmount, balance.decimals);
            // Gas is in ETH (with 18 decimals)
            const gasFeeWei = parseUnits(estimatedGasFee, 18);
            const totalCostWei = amountWei + gasFeeWei;
            setIsAmountValid(totalCostWei <= balance.value);
        }
    }, [balance, currentAmount, estimatedGasFee]);


     // Update the connected account address when it changes
     useEffect(() => {
        setAccount(address as `0x${string}`)
    }, [address]);


     // Handle changes in the amount input field
     const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
        setCurrentAmount(value);
    }
};

    /**
     * Handle form submission for the transfer.
     */
     const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const recipientAddress = resolvedAddress || currentToAddress;

        if (address && currentToAddress) {
            const value = parseUnits(currentAmount, balance?.decimals || 18);
       		if (!isErc20) {

                   // Send native ETH transfer
                    sendTransaction(
                        {
                            to: recipientAddress as `0x${string}`,
                            value: parseUnits(currentAmount, balance?.decimals || 18),
                        })
            } else {

                   // Send ERC20 token transfer
                  writeContract({
					abi: erc20Abi,
					address: tokenAddress as `0x${string}`,
					args: [recipientAddress as `0x${string}`, parseEther(String(value))],
					functionName: "transfer",
				},
				{
					onError: (error) => {
						console.log(error, 111);
					},
				})
            }
        } else {
            setStatus('Wallet is not connected or recipient address is missing');
        }
    };

    // Render the component
    return (
        <div className={styles.transferWidget}>
            <h3>Send</h3>
            <div className={styles.accountInfo}>
                <p>From</p>
                <p>{account || 'Not connected'}</p>
            </div>
            <div className={styles.assetInfo}>
                <div className={styles.assetLabel}>
                    <span>Asset:</span>
                    <span>{token}</span>
                </div>
                <div className={styles.balanceLabel}>
                    <span>Balance:</span>
                    <span>{Number(balance?.formatted || 0).toFixed(2)} {token}</span>
                </div>
            </div>
            <div className={styles.amountInfo}>
                <label>Amount:</label>
                <input
                    type="text"
                    value={currentAmount}
                    onChange={handleAmountChange}
                    placeholder="Enter amount"
                />
            </div>
            <div className={styles.addressInfo}>
                <label>To Address or ENS:</label>
                <input
                    type="text"
                    value={currentToAddress}
                    onChange={(e) => setCurrentToAddress(e.target.value)}
                    placeholder="Enter recipient address or ENS"
                />

            </div>
            <div className={styles.addressInfo}>
                {isResolvingENS && <p>Resolving ENS...</p>}
                {resolvedAddress && <label> Resolved address: </label>}
                {resolvedAddress && <p className={styles.resolvedAddress}> {resolvedAddress}</p>}
            </div>
            <div className={styles.gasFeeInfo}>
                <p>Estimated gas fee</p>
                {isEstimateError ? (
                    <p>Error estimating gas</p>
                ) : (
                    <p>{estimatedGasFee} ETH</p>
                )}
            </div>
            <div className={styles.buttonGroup}>
                <ConnectButton/>
                <button
                    className={styles.transferButton}
                    onClick={handleSubmit}
                    disabled={!account || isPending || isConfirming || !isAmountValid}
                >
                    {isPending ? 'Confirming...' : isConfirming ? 'Processing...' : 'Send'}
                </button>
            </div>
            {!isAmountValid && <p className={styles.errorMessage}>Insufficient balance for transfer and gas fee</p>}
            <div className={styles.status}>{status}</div>
            {hash && (
                <div className={styles.transactionInfo}>
                    <div>Transaction Hash: {hash}</div>
                </div>
            )}
            {isConfirming  && <div className={styles.transactionInfo}>Waiting for confirmation...</div> }
            {isConfirmed && <div className={styles.transactionInfo}>Transaction confirmed.</div>}
            {error && (
                <div className={styles.error}>Error: {(error as BaseError).shortMessage || error.message}</div>
            )}
        </div>
    );
};

/**
 * TransferWidget - Wrapper component that parses URL parameters and renders TransferWidgetComponent.
 */
export function TransferWidget() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token') || '';
    const tokenAddress = params.get('tokenAddress') || '';
    const amount = params.get('amount') || '';
    const toAddress = params.get('toAddress') || '';

    // @ts-ignore
    return (
        <TransferWidgetComponent
            token={token}
            tokenAddress={tokenAddress}
            amount={amount}
            toAddress={toAddress}
        />
    );
}

export default TransferWidget;
