import { atom } from "jotai";
import { proxy } from "valtio";

interface SessionDetailStore extends AiSession {
	abortController?: AbortController;
	status: "error" | "idle" | "pending" | "streaming";
}

export const sessionDetailStore = proxy<Record<string, SessionDetailStore>>({});

export const sessionIdAtom = atom<string | undefined>(undefined);

export const currentIdleTaskAtom = atom<AiTaskItem | undefined>(undefined);
