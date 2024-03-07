type WalletList = WalletListItem[];
interface WalletListItem {
	createTime: string;
	walletAddress: `0x${string}`;
	walletId: number;
}

interface WalletDetail {
	balance: {
		tokenAddress: `0x${string}`;
		/** in wei */
		tokenBalance: string;
		tokenDecimal: number;
		tokenImageUrl: string;
		/** @example "ETH" */
		tokenName: string;
		/** @example "ETH" */
		tokenSymbol: string;
	}[];
	createTime: string;
	walletAddress: `0x${string}`;
	walletId: number;
}
