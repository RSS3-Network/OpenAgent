import { AiSessionMessage } from "@/server/api/routers/ai/types/session";
import { Alert, Avatar, Group, Skeleton } from "@mantine/core";
import { IconBug } from "@tabler/icons-react";
import dynamic from "next/dynamic";
import { useSession } from "next-auth/react";
import { useEffect } from "react";
import { ErrorBoundary } from "react-error-boundary";
import { useSnapshot } from "valtio";

import { isChunkTypeof } from "../chunks/chunk-type-extractor";
import classes from "./index.module.css";

const ToolChunk = dynamic(() =>
	import("../chunks/tool-chunk").then((mod) => mod.ToolChunk)
);
const SuggestedQuestionsChunk = dynamic(() =>
	import("../chunks/suggested-questions-chunk").then(
		(mod) => mod.SuggestedQuestionsChunk
	)
);
const MarkdownChunk = dynamic(
	() => import("../chunks/markdown-chunk").then((mod) => mod.MarkdownChunk),
	{
		loading: (props) => <MessageBodySkeleton role={"human"} />,
	}
);
const PendingLoader = dynamic(() =>
	import("./pending-loader").then((mod) => mod.PendingLoader)
);

export function Message({
	isLastMessage,
	message,
}: {
	isLastMessage: boolean;
	message: AiSessionMessage;
}) {
	useEffect(() => {
		console.log("rerender message", { messageId: message.message_id });
	});

	return (
		<Group
			align="flex-start"
			classNames={{
				root: classes.group,
			}}
			data-role={message.role}
			gap="xs"
			px="md"
			py="lg"
			wrap="nowrap"
		>
			<MessageAvatar message={message} />

			<div className="grow overflow-hidden">
				<MessageBodyWithErrorBoundary
					isLastMessage={isLastMessage}
					message={message}
				/>
			</div>
		</Group>
	);
}

function MessageAvatar({ message }: { message: AiSessionMessage }) {
	const session = useSession();
	const snap = useSnapshot(message);

	const avatarSrc =
		snap.role === "ai" ? "/logo.svg" : session.data?.user?.image;
	const avatarAlt = snap.role === "ai" ? "AI" : "User";

	return (
		<Avatar alt={avatarAlt} mt="8" radius="sm" size="md" src={avatarSrc} />
	);
}

// // TODO: a better way to improve performance
// export const Message = memo(MessageComponent, (prev, next) => {
// 	return (
// 		prev.message.message_id === next.message.message_id && !prev.isLastMessage
// 	);
// });

function MessageBody({
	isLastMessage,
	message,
}: {
	isLastMessage: boolean;
	message: AiSessionMessage;
}) {
	const content = useSnapshot(message.content);

	const sqChunk = content.find((chunk) =>
		isChunkTypeof(chunk as any, "suggested_questions")
	);

	return (
		<>
			{content.map((chunk, i) => {
				return (
					<ContentRenderer
						chunk={message.content[i]}
						isLastMessage={isLastMessage}
						key={chunk.block_id}
					/>
				);
			})}

			{isLastMessage && sqChunk && (
				<SuggestedQuestionsChunk questions={(sqChunk as any)?.body} />
			)}

			{/* pending status */}
			<PendingLoader isLastMessage={isLastMessage} />
		</>
	);
}

function ContentRenderer({
	chunk,
	isLastMessage,
}: {
	chunk: AiSessionMessage["content"][number];
	isLastMessage: boolean;
}) {
	if (isChunkTypeof(chunk, "tool")) {
		return (
			<div>
				<ToolChunk chunk={chunk} />
			</div>
		);
	}

	if (isChunkTypeof(chunk, "natural_language")) {
		return (
			<div className="mt-4">
				<MarkdownChunk chunk={chunk} />
			</div>
		);
	}

	// if (isLastMessage && isChunkTypeof(chunk, "suggested_questions")) {
	// 	return (
	// 		<div>
	// 			<SuggestedQuestionsChunk questions={chunk.body} />
	// 		</div>
	// 	);
	// }
}

function MessageBodyWithErrorBoundary({
	isLastMessage,
	message,
}: {
	isLastMessage: boolean;
	message: AiSessionMessage;
}) {
	return (
		<ErrorBoundary
			fallbackRender={(props) => (
				<Alert
					color="red"
					icon={<IconBug />}
					title="Sorry! Something wrong."
					variant="light"
				>
					I&apos;m really sorry about this. This message is not available
					because of an error. You may report this issue to our support team on
					Discord.
					<br />
					Error message: {props.error.message}
				</Alert>
			)}
		>
			<MessageBody isLastMessage={isLastMessage} message={message} />
		</ErrorBoundary>
	);
}

export function MessageSkeleton({ role }: { role: AiSessionMessage["role"] }) {
	return (
		<Group
			align="flex-start"
			classNames={{
				root: classes.group,
			}}
			data-role={role}
			gap="xs"
			px="md"
			py="lg"
			wrap="nowrap"
		>
			<Skeleton
				circle
				height="calc(2.375rem*var(--mantine-scale))"
				width="calc(2.375rem*var(--mantine-scale))"
			>
				{/* <Avatar mt="8" size="md" radius="xl" /> */}
			</Skeleton>

			<div className="grow overflow-hidden">
				<MessageBodySkeleton role={"human"} />
			</div>
		</Group>
	);
}

function MessageBodySkeleton({ role }: { role: AiSessionMessage["role"] }) {
	return (
		<>
			<Skeleton mt="sm">
				<p></p>
			</Skeleton>
			<Skeleton mt="sm">
				<p></p>
			</Skeleton>
			<Skeleton mt="sm">
				<p></p>
			</Skeleton>
			{role === "ai" && (
				<>
					<Skeleton mt="sm">
						<p></p>
					</Skeleton>
					<Skeleton mt="sm">
						<p></p>
					</Skeleton>
					<Skeleton mt="sm">
						<p></p>
					</Skeleton>
				</>
			)}
			<Skeleton mt="sm" w="80%">
				<p></p>
			</Skeleton>
		</>
	);
}
