import { Text } from "@mantine/core";

export function Label({ children }: { children: string }) {
	return <Text fw="bold">{children}</Text>;
}
