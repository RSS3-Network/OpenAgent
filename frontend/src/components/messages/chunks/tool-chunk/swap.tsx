import { AiSessionMessageToolOutputBody_Swap } from "@/server/api/routers/ai/types/session";
import { LiFiWidget, WidgetConfig } from "@lifi/widget";
import { IconInfoCircle } from "@tabler/icons-react";

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
	expired,
}: {
	body: AiSessionMessageToolOutputBody_Swap;
	expired: boolean;
}) {
	return expired ? (
		<div className="flex items-center gap-2 rounded-sm bg-gray-300 px-4 py-2">
			<IconInfoCircle className="h-5 w-5" />
			The swap has expired.
		</div>
	) : (
		<ShowUpItem index={0}>
			<LiFiWidget
				config={{
					...widgetConfig,
					fromAmount: body.amount,
					fromChain: Number(body.chain_id),
					fromToken: body.from_token,
					toChain: Number(body.chain_id),
					toToken: body.to_token,
				}}
				integrator={widgetConfig.integrator}
			/>
		</ShowUpItem>
	);
}
