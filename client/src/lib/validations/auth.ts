import { email, object, string } from "valibot";

export const userAuthSchema = object({
	email: string([email()]),
});
