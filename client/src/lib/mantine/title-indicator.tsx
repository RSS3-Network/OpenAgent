"use client";

import { useEffect, useState } from "react";

export function TitleIndicator() {
	if (process.env.NODE_ENV === "production" || typeof window === "undefined")
		return null;

	return <TitleIndicator_ />;
}

function TitleIndicator_() {
	const [title, setTitle] = useState(window.document.title);
	const [isMounted, setIsMounted] = useState(false);

	useEffect(() => {
		setIsMounted(true);
		const target = document.querySelector("head > title")!;
		const observer = new window.MutationObserver(function (mutations) {
			mutations.forEach(function (mutation) {
				// console.log("new title:", mutation.target.textContent);
				setTitle(mutation.target.textContent!);
			});
		});
		observer.observe(target, {
			characterData: true,
			childList: true,
			subtree: true,
		});

		return () => {
			observer.disconnect();
		};
	}, []);

	return (
		isMounted && (
			<div className="fixed left-1 top-1 z-[9999] flex h-6 w-fit items-center justify-center bg-gray-800 p-3 font-mono text-xs text-white opacity-30 hover:opacity-100 dark:bg-gray-100 dark:text-black">
				{title}
			</div>
		)
	);
}
