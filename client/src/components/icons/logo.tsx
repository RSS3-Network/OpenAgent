import { rem } from "@mantine/core";
import { forwardRef } from "react";

interface IconLogoProps extends React.ComponentPropsWithoutRef<"svg"> {
	size?: number | string;
}

export const IconLogo = forwardRef<SVGSVGElement, IconLogoProps>(
	({ size, style, ...props }, ref) => {
		return (
			<svg
				fill="none"
				// height="300"
				ref={ref}
				style={{ height: rem(size), width: rem(size), ...style }}
				viewBox="0 0 300 300"
				// width="300"
				xmlns="http://www.w3.org/2000/svg"
				{...props}
			>
				<rect fill="#E7352E" height="300" rx="40" width="300" />
				<path
					d="M50 70C50 58.9543 58.9543 50 70 50H300V250H70C58.9543 250 50 241.046 50 230V70Z"
					fill="black"
				/>
				<rect fill="white" height="60" rx="10" width="25" x="150" y="160" />
				<rect fill="white" height="60" rx="10" width="25" x="220" y="160" />
			</svg>
		);
	}
);
IconLogo.displayName = "IconLogo";
