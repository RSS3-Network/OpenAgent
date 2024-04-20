import "./src/env.mjs"; // validate at build time

import million from "million/compiler";

const withBundleAnalyzer = await import("@next/bundle-analyzer").then((mod) =>
	mod.default({ enabled: process.env.ANALYZE === "true" })
);

/** @type {import('next').NextConfig} */
const nextConfig = {
	experimental: {
		optimizePackageImports: [
			"@mantine/core",
			"@mantine/hooks",
			"@tabler/icons-react",
		],
		// swcPlugins: [["@swc-jotai/react-refresh", {}]],
	},
	webpack: (config) => {
		config.resolve.fallback = { fs: false, net: false, tls: false };
		config.externals.push("pino-pretty", "lokijs", "encoding");
		return config;
	},
};

/** @type {Parameters<million['next']>[1]} */
const millionConfig = {
	auto: { rsc: true },
};

export default million.next(withBundleAnalyzer(nextConfig), millionConfig);
// export default withBundleAnalyzer(nextConfig);
