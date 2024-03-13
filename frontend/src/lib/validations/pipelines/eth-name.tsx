import {
	type BaseValidation,
	type ErrorMessage,
	actionIssue,
	actionOutput,
} from "valibot";

export type EthAddressValidation<TInput extends string> =
	BaseValidation<TInput> & {
		requirement: RegExp;
		type: "eth_name";
	};

/**
 * @example "songkeys.eth" (always ends with ".eth")
 */
export function ethName<TInput extends string>(
	message: ErrorMessage = "Invalid ENS"
): EthAddressValidation<TInput> {
	return {
		_parse(input) {
			return !this.requirement.test(input)
				? actionIssue(this.type, this.message, input)
				: actionOutput(input);
		},
		async: false,
		message,
		requirement: /^[a-zA-Z0-9-]+\.eth$/,
		type: "eth_name",
	};
}
