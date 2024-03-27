import { SessionProvider } from "@/lib/auth";
import { JotaiProvider } from "@/lib/jotai";
import { MantineProvider } from "@/lib/mantine";
import { MotionProvider } from "@/lib/motion";
import { TrpcProvider } from "@/lib/trpc";
import { WagmiProvider } from "@/lib/wagmi";
import { RainbowKitProvider } from "@/lib/wagmi/provider";
import { headers } from "next/headers";
import { type PropsWithChildren } from "react";

export function Providers({ children }: PropsWithChildren<{}>) {
	return (
		<WagmiProvider>
			<TrpcProvider headers={headers()}>
				<RainbowKitProvider>
					<MantineProvider>
						<SessionProvider>
							<JotaiProvider>
								<MotionProvider>{children}</MotionProvider>
							</JotaiProvider>
						</SessionProvider>
					</MantineProvider>
				</RainbowKitProvider>
			</TrpcProvider>
		</WagmiProvider>
	);
}
