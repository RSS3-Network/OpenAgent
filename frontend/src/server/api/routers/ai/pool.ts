import { env } from "@/env.mjs";
import { Pool } from "undici";

export const pool = new Pool(env.BACKEND_URL, {
  connections: 50,
});
