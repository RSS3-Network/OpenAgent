type AiTaskStatus =
	| "canceled"
	| "done"
	| "failed"
	| "idle"
	| "pending"
	| "running";

type AiTaskType = "transfer";

interface AiTaskItem<T extends AiTaskType = AiTaskType> {
	body: AiTaskItemBody<T>;
	created_at: string;
	done_at: string;
	hash?: `0x${string}`;
	run_at: string;
	session_id: string;
	status: AiTaskStatus;
	task_id: string;
	type: T;
	user_id: string;
}

type AiTaskItemBody<T extends AiTaskType = AiTaskType> =
	AiTaskItemBody_Type_Content_Mapping[T];

/**
 * @private
 */
type AiTaskItemBody_Type_Content_Mapping = {
	transfer: AiTaskItemBody_Transfer;
};

interface AiTaskItemBody_Transfer {
	/** in eth */
	amount: string;
	decimals: number;
	logoURI: string;
	to_address: `${string}.eth` | `0x${string}`;
	token: string;
	token_address: `0x${string}`;
	executor_id: number;
}

type AiTaskItemList = AiTaskItem[];
