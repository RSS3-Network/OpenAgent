import type { ReactNode } from "react";

import { Box, Text, rem } from "@mantine/core";
import {
	IconActivity,
	IconBrandAppstore,
	IconCurrencyEthereum,
	IconFlame,
	IconGasStation,
	IconLineHeight,
	IconMoodSmile,
	IconQuestionMark,
	IconSearch,
	IconUser,
	IconUsersGroup,
} from "@tabler/icons-react";

import { QuestionCards } from "./question-cards";

const Bold = ({ children }: { children: ReactNode }) => (
	<Text fw="bold" span>
		{children}
	</Text>
);

const iconStyle = { height: rem(24), width: rem(24) };

const suggestedQuestions = [
	{
		icon: <IconCurrencyEthereum style={iconStyle} />,
		plaintext: "Tell me about Ethereum.",
		question: (
			<>
				Tell me about <Bold>Ethereum</Bold>.
			</>
		),
	},
	{
		icon: <IconCurrencyEthereum style={iconStyle} />,
		plaintext: "What is the current price of ETH?",
		question: (
			<>
				What is the <Bold>current price</Bold> of ETH?
			</>
		),
	},
	{
		icon: <IconFlame style={iconStyle} />,
		plaintext: "Can you list some hot tokens?",
		question: (
			<>
				Can you list some <Bold>hot tokens</Bold>?
			</>
		),
	},
	{
		icon: <IconFlame style={iconStyle} />,
		plaintext: "Can you list some hot NFTs?",
		question: (
			<>
				Can you list some <Bold>hot NFTs</Bold>?
			</>
		),
	},
	{
		icon: <IconActivity style={iconStyle} />,
		plaintext: "What did vitalik.eth do recently?",
		question: (
			<>
				What did <Bold>vitalik.eth</Bold> do recently?
			</>
		),
	},
	{
		icon: <IconLineHeight style={iconStyle} />,
		plaintext: "What is the current block height?",
		question: (
			<>
				What is the <Bold>current block height</Bold>?
			</>
		),
	},
	{
		icon: <IconGasStation style={iconStyle} />,
		plaintext: "What is the current gas price?",
		question: (
			<>
				What is the <Bold>current gas price</Bold>?
			</>
		),
	},
	{
		icon: <IconUsersGroup style={iconStyle} />,
		plaintext: "List the most active users on Ethereum.",
		question: (
			<>
				List the <Bold>most active users</Bold> on Ethereum.
			</>
		),
	},
	{
		icon: <IconQuestionMark style={iconStyle} />,
		plaintext: "What is the difference between Arbitrum and Ethereum?",
		question: (
			<>
				What is the difference between <Bold>Arbitrum</Bold> and{" "}
				<Bold>Ethereum</Bold>?
			</>
		),
	},
	{
		icon: <IconQuestionMark style={iconStyle} />,
		plaintext: "How can I get some ETH?",
		question: (
			<>
				How can I get some <Bold>ETH</Bold>?
			</>
		),
	},
	{
		icon: <IconBrandAppstore style={iconStyle} />,
		plaintext: "What are the top dapps in Ethereum?",
		question: (
			<>
				What are the top <Bold>dapps</Bold> in Ethereum?
			</>
		),
	},
	{
		icon: <IconSearch style={iconStyle} />,
		plaintext: "List some DeFi projects having the highest TVL.",
		question: (
			<>
				List some <Bold>DeFi projects</Bold> having the highest TVL.
			</>
		),
	},
	{
		icon: <IconUser style={iconStyle} />,
		plaintext: "Who is vitalik.eth on Ethereum?",
		question: (
			<>
				Who is <Bold>vitalik.eth</Bold> on Ethereum?
			</>
		),
	},
	{
		icon: <IconMoodSmile style={iconStyle} />,
		plaintext: "Who are you?",
		question: <>Who are you?</>,
	},
	{
		icon: <IconMoodSmile style={iconStyle} />,
		plaintext: "Who built you?",
		question: <>Who built you?</>,
	},
];

export function NewSessionGuide({ sessionId }: { sessionId: string }) {
	const randomSixQuestions = suggestedQuestions
		.sort(() => 0.5 - Math.random())
		.slice(0, 6);

	return (
		<Box bottom={rem(80)} pos="absolute" px="md">
			<QuestionCards questions={randomSixQuestions} sessionId={sessionId} />
		</Box>
	);
}
