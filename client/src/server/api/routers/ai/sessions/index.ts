import { createTRPCRouter } from "@/lib/trpc/server";

import { createFavoriteFolderApi } from "./create-favorite-folder";
import { deleteSessionApi } from "./delete";
import { detailSessionApi } from "./detail";
import { favoriteSessionsApi } from "./favorites";
import { recentSessionsApi } from "./recents";
import { updateSessionApi } from "./update";

export const sessionsRouter = createTRPCRouter({
	createFavoriteFolder: createFavoriteFolderApi,
	delete: deleteSessionApi,
	detail: detailSessionApi,
	favorites: favoriteSessionsApi,
	recents: recentSessionsApi,
	update: updateSessionApi,
});
