import {
	type BaseValidation,
	type ErrorMessage,
	actionIssue,
	actionOutput,
} from "valibot";

export type EthAddressValidation<TInput extends string> =
	BaseValidation<TInput> & {
		requirement: RegExp;
		type: "eth_address";
	};

export function ethAddress<TInput extends string>(
	message: ErrorMessage = "Invalid address"
): EthAddressValidation<TInput> {
	return {
		_parse(input) {
			return !this.requirement.test(input)
				? actionIssue(this.type, this.message, input)
				: actionOutput(input);
		},
		async: false,
		message,
		requirement: /^0x[a-fA-F0-9]{40}$/,
		type: "eth_address",
	};
}
