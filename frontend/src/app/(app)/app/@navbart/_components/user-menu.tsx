"use client";

import { Avatar, Group, Menu, Text, UnstyledButton } from "@mantine/core";
import { signOut } from "next-auth/react";
import { forwardRef } from "react";

import { LayoutBurger } from "../../_components/layout-burger";
import classes from "./user-menu.module.css";

function UserCard({
	email,
	image,
	username,
	withBurger = false,
}: {
	withBurger?: boolean;
} & UserButtonProps) {
	return (
		<Group className="overflow-hidden" wrap="nowrap">
			<Avatar radius="xl" src={image} />

			<div className="flex-1 overflow-hidden">
				<Text className="select-none" fw={500} size="sm" truncate="end">
					{username}
				</Text>

				<Text c="dimmed" className="select-none" size="xs" truncate="end">
					{email}
				</Text>
			</div>

			{withBurger && <LayoutBurger />}
		</Group>
	);
}

interface UserButtonProps extends React.ComponentPropsWithoutRef<"div"> {
	email?: null | string;
	image?: null | string;
	username?: null | string;
}

const UserButton = forwardRef<HTMLDivElement, UserButtonProps>(
	({ email, image, username, ...props }: UserButtonProps, ref) => (
		<Group justify="space-between" w="100%">
			<Group className="flex-1 overflow-hidden">
				<UnstyledButton
					classNames={{
						root: classes["user-button"],
					}}
					component="div"
					p="xs"
					ref={ref}
					role="button"
					w="100%"
					{...props}
				>
					<UserCard
						email={email}
						image={image}
						username={username}
						withBurger
					/>
				</UnstyledButton>
			</Group>
		</Group>
	)
);
UserButton.displayName = "UserButton";

interface UserMenuProps {
	email?: null | string;
	image?: null | string;
	username?: null | string;
}
export function UserMenu({ email, image, username }: UserMenuProps) {
	return (
		<Menu
			offset={{
				crossAxis: 25,
				mainAxis: 5,
			}}
			position="bottom"
			shadow="md"
			width={330}
		>
			<Menu.Target>
				<UserButton email={email} image={image} username={username} />
			</Menu.Target>
			<Menu.Dropdown>
				<Menu.Label>
					<Text size="xs" truncate="end">
						{username || email}
					</Text>
				</Menu.Label>

				<Menu.Item>
					<UserCard email={email} image={image} username={username} />
				</Menu.Item>

				<Menu.Divider />

				<Menu.Item
					color="red"
					onClick={() => {
						signOut();
					}}
				>
					Logout
				</Menu.Item>
			</Menu.Dropdown>
		</Menu>
	);
}
