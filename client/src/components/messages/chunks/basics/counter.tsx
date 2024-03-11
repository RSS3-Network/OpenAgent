import { animate } from "framer-motion";
import { useEffect, useRef } from "react";

export function Counter({
	decimals = 0,
	from,
	to,
}: {
	decimals?: number;
	from: number;
	to: number;
}) {
	const nodeRef = useRef(null);

	useEffect(() => {
		const node = nodeRef.current;
		const controls = animate(from, to, {
			duration: 1,
			onUpdate(value) {
				if (node) {
					// @ts-ignore
					node.textContent = parseFloat(
						value.toFixed(decimals)
					).toLocaleString();
				}
			},
		});

		return () => controls.stop();
	}, [decimals, from, to]);

	return <span ref={nodeRef} />;
}
