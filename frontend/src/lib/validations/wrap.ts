import {
	wrap as _wrap,
	Infer,
	InferIn,
	Schema,
	TypeSchema,
} from "@decs/typeschema";
import { ValiError } from "valibot";

export function wrap<TSchema extends Schema>(
	schema: TSchema
): TypeSchema<Infer<TSchema>, InferIn<TSchema>> {
	return {
		..._wrap(schema),
		parse: async (data) => {
			try {
				return await _wrap(schema).parse(data);
			} catch (err: any) {
				// TODO: remove @decs/typeschema specific error handling
				// https://github.com/decs/typeschema/blob/6a8f0d9ce9435ba9babcb370724660aaa3c27305/src/validation.ts#L32C25-L32C25
				if (err.message === "Assertion failed") {
					throw new ValiError(err.errors);
				}
				throw err;
			}
		},
	};
}
