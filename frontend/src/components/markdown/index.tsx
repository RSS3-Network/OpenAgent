import { TypographyStylesProvider } from "@mantine/core";
import dynamic from "next/dynamic";
import { default as _Markdown } from "react-markdown";
import remarkGfm from "remark-gfm";

const CodeHighlight = dynamic(
	() => import("./code-highlight").then((mod) => mod.CodeHighlight),
	{
		loading: () => <p>Loading code...</p>,
	}
);

export function Markdown({ children }: { children: string }) {
	return (
		<TypographyStylesProvider pl="0" w="100%">
			<_Markdown
				components={{
					code(props) {
						const { children, className, node, ...rest } = props;
						const match = /language-(\w+)/.exec(className || "");
						return match ? (
							<CodeHighlight
								{...rest}
								code={String(children)}
								language={match[1]}
							/>
						) : (
							<code {...rest} className={className}>
								{children}
							</code>
						);
					},
				}}
				remarkPlugins={[remarkGfm]}
			>
				{children}
			</_Markdown>
		</TypographyStylesProvider>
	);
}
