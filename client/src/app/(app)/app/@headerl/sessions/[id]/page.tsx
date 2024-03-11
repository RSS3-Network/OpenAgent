import { SessionTitle } from "./_components/session-title";

export default function Page({
	params,
	searchParams,
}: {
	params: { id: string };
	searchParams: {
		new?: "true";
	};
}) {
	const isNewChat = searchParams.new === "true";

	return (
		<>
			<SessionTitle isNewChat={isNewChat} sessionId={params.id} />
		</>
	);
}
