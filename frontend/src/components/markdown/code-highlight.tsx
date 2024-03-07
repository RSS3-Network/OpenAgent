import { CodeHighlight as _CodeHighlight } from "@mantine/code-highlight";
import "@mantine/code-highlight/styles.css";

import "./code-highlight.css";

export function CodeHighlight({
	code,
	language,
}: {
	code: string;
	language: string;
}) {
	return <_CodeHighlight code={code} language={language} />;
}
