import { useAiIsCurrentSession, useAiSessionTitle } from "@/lib/ai/hooks";
import { api } from "@/lib/trpc/client";
import { TextInput } from "@mantine/core";
import { getHotkeyHandler, useInputState } from "@mantine/hooks";
import { IconMessageCircle } from "@tabler/icons-react";

export function SessionLinkRename({
	defaultTitle,
	onSubmit,
	session,
}: {
	defaultTitle: string;
	onSubmit: (title: string) => void;
	session: AiSessionListItem;
}) {
	const [title, setTitle] = useInputState(defaultTitle);
	const { isCurrentSession } = useAiIsCurrentSession(session.session_id);
	const { setSessionTitle: setCurrentSessionTitle } = useAiSessionTitle({
		sessionId: session.session_id,
	});

	const utils = api.useUtils();
	const updateSession = api.ai.sessions.update.useMutation({
		onError() {
			// TODO:
		},
		async onMutate() {
			await utils.ai.sessions.recents.cancel({});
			await utils.ai.sessions.favorites.cancel();
			if (isCurrentSession) {
				setCurrentSessionTitle(title);
			}
		},
		async onSettled() {
			await utils.ai.sessions.invalidate();
		},
	});

	const handleSubmit = () => {
		onSubmit(title);
		if (title !== defaultTitle) {
			updateSession.mutate({
				sessionId: session.session_id,
				title,
			});
		}
	};

	return (
		<div>
			<TextInput
				leftSection={<IconMessageCircle />}
				onBlur={handleSubmit}
				onChange={setTitle}
				onKeyDown={getHotkeyHandler([["Enter", handleSubmit]])}
				placeholder="Title..."
				value={title}
			/>
		</div>
	);
}
