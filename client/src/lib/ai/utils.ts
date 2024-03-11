/**
 * Returns a new session href
 * @example "/app/sessions/1234-5678-9012-3456?new=true"
 */
export function getNewSessionHref() {
	return `/app/sessions/${crypto.randomUUID()}?new=true`;
}

export function getOnboardingHref() {
	return `/app/sessions/${crypto.randomUUID()}?onboarding=true&new=true`;
}
