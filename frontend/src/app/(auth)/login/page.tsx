import { IconLogo } from "@/components/icons";
import { auth } from "@/lib/auth";
import { IconArrowLeft } from "@tabler/icons-react";
import { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { UserAuthForm } from "./user-auth-form.client";

export const metadata: Metadata = {
	description: "Login to your account",
	title: "Login",
};

export default async function LoginPage({
	searchParams,
}: {
	searchParams?: { from?: string };
}) {
	const session = await auth();
	if (session) {
		redirect(searchParams?.from ?? "/app");
	}

	return (
		<div className="container mx-auto flex h-screen w-screen flex-col items-center justify-center">
			<Link className="absolute left-4 top-4 md:left-8 md:top-8" href="/">
				<>
					<IconArrowLeft className="mr-2 size-4" />
					Back
				</>
			</Link>
			<div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[400px]">
				<div className="flex flex-col space-y-2 text-center">
					<IconLogo className="mx-auto size-10" />
					<h1 className="text-2xl font-semibold tracking-tight">
						Welcome to OpenAgent
					</h1>
					<p className="text-sm">
						Enter your email to sign in to your account,
						<br />
						If you don&apos;t have an account, we&apos;ll create one for you.
					</p>
				</div>
				<UserAuthForm />
				{/* <p className="px-8 text-center text-sm text-muted-foreground">
					<Link
						href="/register"
						className="hover:text-brand underline underline-offset-4"
					>
						Don&apos;t have an account? Sign Up
					</Link>
				</p> */}
			</div>
		</div>
	);
}
