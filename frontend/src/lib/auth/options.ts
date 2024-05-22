import type { DefaultSession } from "next-auth";

import { env } from "@/env.mjs";
import { PrismaAdapter } from "@auth/prisma-adapter";
import NextAuth from "next-auth";
import DiscordProvider from "next-auth/providers/discord";
import EmailProvider from "next-auth/providers/email";
import GoogleProvider from "next-auth/providers/google";

import { db } from "../db";
// import "server-only";

/**
 * Module augmentation for `next-auth` types. Allows us to add custom properties to the `session`
 * object and keep type safety.
 *
 * @see https://next-auth.js.org/getting-started/typescript#module-augmentation
 */
declare module "next-auth" {
	interface Session extends DefaultSession {
		user: {
			id: string;
			// ...other properties
			// role: UserRole;
		} & DefaultSession["user"];
	}

	// interface User {
	//   // ...other properties
	//   // role: UserRole;
	// }
}

export const {
	auth,
	handlers: { GET, POST },
} = NextAuth({
	adapter: PrismaAdapter(db),
	callbacks: {
		session: ({ session, user }) => ({
			...session,
			user: {
				...session.user,
				id: user.id,
			},
		}),
	},
	pages: {
		// signIn: "/login",
	},
	providers: [
		GoogleProvider({
			// https://next-auth.js.org/providers/google#configuration
			authorization: {
				params: {
					access_type: "offline",
					prompt: "consent",
					response_type: "code",
				},
			},
			clientId: env.AUTH_GOOGLE_CLIENT_ID,
			clientSecret: env.AUTH_GOOGLE_CLIENT_SECRET,
		}),
		EmailProvider({
			from: `"OpenAgent" <${env.AUTH_GMAIL_USER}>`,
			// generateVerificationToken: () => {
			// 	return "test-token";
			// },
			// https://nodemailer.com/#example
			server: {
				auth: {
					pass: env.AUTH_GMAIL_PASS,
					user: env.AUTH_GMAIL_USER,
				},
				host: "smtp.gmail.com",
				port: 587,
				secure: false,
				service: "gmail",
			},
		}),
		DiscordProvider({
			clientId: env.AUTH_DISCORD_CLIENT_ID,
			clientSecret: env.AUTH_DISCORD_CLIENT_SECRET,
		}),
	],
	session: {
		strategy: "database",
	},
	trustHost: true,
});
