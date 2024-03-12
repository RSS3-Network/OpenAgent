"use client";

import { IconLogo } from "@/components/icons";
import { api } from "@/lib/trpc/client";
import { Button, Text } from "@mantine/core";
import { IconWallet } from "@tabler/icons-react";

import { PageModal } from "../../_components/page-modal";

export function OnboardingModal() {
	const utils = api.useUtils();
	const executorCreate = api.executor.executorCreate.useMutation();

	return (
		<PageModal closeOnClickOutside={false}>
			{({ close }) => (
				<>
					<Text my="md">
						Hi! Welcome to use <IconLogo className="align-middle" size="1rem" />{" "}
						OpenAgent.
					</Text>

					<Text my="md">
						OpenAgent can help you to manage your crypto assets and track your
						portfolio.
					</Text>

					<Text my="md">
						Let&apos;s get started by setting up your first{" "}
						<IconWallet className="align-middle" size="1rem" />
						<Text fw={700} span>
							executor
						</Text>{" "}
						with a simple click.
					</Text>

					<Button
						fullWidth
						loading={executorCreate.isPending}
						mt="md"
						onClick={() =>
							executorCreate.mutate(undefined, {
								onSuccess: async () => {
									await utils.executor.executors.invalidate();
									close();
								},
							})
						}
						size="md"
					>
						Create Executor
					</Button>

					<Button
						disabled={executorCreate.isPending}
						fullWidth
						mt="sm"
						onClick={() => close()}
						size="md"
						variant="subtle"
					>
						Do It Later
					</Button>

					<Text my="sm" size="xs">
						*You can always create a executor later in the settings page.
					</Text>
				</>
			)}
		</PageModal>
	);
}
