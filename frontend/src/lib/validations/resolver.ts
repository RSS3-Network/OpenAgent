import { type FormErrors } from "@mantine/form";
import { type BaseSchema, type ValiError, parse } from "valibot";

export function valibotResolver<T extends Record<string, unknown>>(
	schema: BaseSchema<T>
) {
	return (values: T): FormErrors => {
		try {
			parse(schema, values);

			return {};
		} catch (errors) {
			const results = (errors as ValiError).issues
				.filter(
					(
						error
					): error is ValiError["issues"][number] & {
						path: { key: string }[];
					} => Boolean(error.path)
				)
				.reduce<FormErrors>((acc, error) => {
					const key = error.path.map((p) => p.key).join(".");
					acc[key] = error.message;
					return acc;
				}, {});
			return results;
		}
	};
}
