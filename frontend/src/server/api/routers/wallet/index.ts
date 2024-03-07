import { createTRPCRouter } from "@/lib/trpc/server";

import { walletApi } from "./wallet";
import { walletCreateApi } from "./wallet-create";
import { walletsApi } from "./wallets";

export const walletRouter = createTRPCRouter({
	wallet: walletApi,
	walletCreate: walletCreateApi,
	wallets: walletsApi,
});
