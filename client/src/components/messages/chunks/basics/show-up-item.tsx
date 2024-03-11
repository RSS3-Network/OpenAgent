import { m } from "framer-motion";

export function ShowUpItem({
	children,
	index,
}: {
	children: React.ReactNode;
	index: number;
}) {
	return (
		<m.div
			animate={{ opacity: 1, y: 0 }}
			className="flex items-stretch justify-stretch"
			exit={{ opacity: 0, y: 10 }}
			initial={{ opacity: 0, y: 10 }}
			transition={{ delay: index * 0.2 }}
		>
			{children}
		</m.div>
	);
}
