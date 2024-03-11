import {
	type BaseValidation,
	type ErrorMessage,
	actionIssue,
	actionOutput,
} from "valibot";

export type TokenAmountValidation<
	TInput extends string,
	TRequirement extends number
> = BaseValidation<TInput> & {
	/**
	 * Decimals
	 */
	requirement: TRequirement;
	type: "token_amount";
};

/**
 * @example "songkeys.eth" (always ends with ".eth")
 */
export function ethName<TInput extends string, TRequirement extends number>(
	requirement: TRequirement,
	message: ErrorMessage = "Invalid number"
): TokenAmountValidation<TInput, TRequirement> {
	return {
		_parse(input) {
			return new RegExp(`^\\d+(\\.\\d{1,${requirement}})?$`).test(input)
				? actionIssue(this.type, this.message, input)
				: actionOutput(input);
		},
		async: false,
		message,
		requirement,
		type: "token_amount",
	};
}
