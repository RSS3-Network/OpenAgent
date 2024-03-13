import { env } from "@/env.mjs";
import { Pool } from "undici";

export const pool = new Pool(env.API_EXECUTOR_URL, {
	connections: 50,
});
