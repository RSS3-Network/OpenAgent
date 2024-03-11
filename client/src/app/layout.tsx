import type { Metadata, Viewport } from "next";

import { Providers } from "@/components/providers";
import { env } from "@/env.mjs";
import { ColorSchemeScript } from "@/lib/mantine";
import { Inter } from "next/font/google";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
	description: "AI that executes",
	keywords: ["ai", "open-agent", "web3", "ethereum", "smart contracts", "nft"],
	metadataBase: new URL(env.NEXTAUTH_URL),
	openGraph: {
		description: "AI that executes",
		images: ["/og.png"],
		locale: "en_US",
		siteName: "OpenAgent",
		title: "OpenAgent",
		type: "website",
		url: env.NEXTAUTH_URL,
	},
	title: "OpenAgent",
	twitter: {
		card: "summary_large_image",
		description: "AI that executes",
		images: ["/og.png"],
		title: "OpenAgent",
	},
};

export const viewport: Viewport = {
	themeColor: [
		{ color: "white", media: "(prefers-color-scheme: light)" },
		{ color: "black", media: "(prefers-color-scheme: dark)" },
	],
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en">
			<head>
				<ColorSchemeScript />
			</head>
			<body className={inter.className}>
				<Providers>{children}</Providers>
			</body>
		</html>
	);
}
