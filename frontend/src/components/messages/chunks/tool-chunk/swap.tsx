import { LiFiWidget, WidgetConfig } from "@lifi/widget";

import { ShowUpItem } from "../basics/show-up-item";

const widgetConfig: WidgetConfig = {
	containerStyle: {
		border: "1px solid rgb(234, 234, 234)",
		borderRadius: "16px",
	},
	integrator: "OpenAgent",
};

export function ToolChunkSwap({
	body,
}: {
	body: AiSessionMessageToolInputBody_Swap;
}) {
	return (
		<ShowUpItem index={0}>
			<LiFiWidget
				config={{
					...widgetConfig,
					fromAmount: body.amount,
					fromToken: body.from_token,
					toToken: body.to_token,
				}}
				integrator={widgetConfig.integrator}
			/>
		</ShowUpItem>
	);
}
