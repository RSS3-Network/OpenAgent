"use client";

import { Modal as Modal_, ModalProps } from "@mantine/core";
// import { useDocumentTitle } from "@mantine/hooks";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

export function PageModal(
	props: Omit<ModalProps, "children" | "onClose" | "opened"> & {
		children:
			| (({ close }: { close: () => void }) => React.ReactNode)
			| React.ReactNode;
		// documentTitle: string;
	}
) {
	const { children, ...rest } = props;

	// useDocumentTitle(documentTitle);

	const router = useRouter();
	const backTimer = useRef<NodeJS.Timeout>();
	const [status, setStatus] = useState<"closed" | "idle" | "opened">("idle");

	useEffect(() => {
		let timeout: NodeJS.Timeout;
		if (status === "idle") {
			timeout = setTimeout(() => {
				setStatus("opened");
			}, 50);
		}
		return () => {
			clearTimeout(timeout);
		};
	}, [status]);

	useEffect(() => {
		return () => {
			backTimer.current && clearTimeout(backTimer.current);
		};
	}, []);

	const back = () => {
		setStatus("closed");
		backTimer.current = setTimeout(() => {
			router.back();
		}, 50);
	};

	return (
		<Modal_
			centered
			onClose={back}
			opened={status === "opened"}
			withCloseButton={false}
			{...rest}
		>
			{typeof children === "function" ? children({ close: back }) : children}
		</Modal_>
	);
}
