type ExecutorList = ExecutorListItem[];
interface ExecutorListItem {
	createTime: string;
	executorAddress: `0x${string}`;
	executorId: number;
}

interface ExecutorDetail {
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
	executorAddress: `0x${string}`;
	executorId: number;
}
