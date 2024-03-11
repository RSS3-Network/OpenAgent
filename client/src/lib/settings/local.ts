import { useLocalStorage } from "@mantine/hooks";
import superjson from "superjson";

interface LocalSettings {
	"interface.navbar.width": number;
}

const DEFAULT_LOCAL_SETTINGS: LocalSettings = {
	"interface.navbar.width": 300,
};

const PREFIX = "open-agent.local-settings";

export function useLocalSettings<T extends keyof LocalSettings>(
	key: T
): [LocalSettings[T], (value: LocalSettings[T]) => void] {
	const [value, setValue] = useLocalStorage<LocalSettings[T]>({
		defaultValue: DEFAULT_LOCAL_SETTINGS[key],
		deserialize: (str) =>
			str === undefined ? DEFAULT_LOCAL_SETTINGS[key] : superjson.parse(str),
		getInitialValueInEffect: true, // for SSR
		key: `${PREFIX}.${key}`,
		serialize: superjson.stringify,
	});

	return [value!, setValue];
}
