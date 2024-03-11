/**
 * @example truncateAddress('0x1234567890abcdef1234567890abcdef12345678')
 * // '0x1234...5678'
 */
export function truncateAddress(address: `${string}.eth` | `0x${string}`) {
	if (!address) return "";
	if (address.endsWith(".eth")) {
		return address;
	}
	return `${address.slice(0, 6)}...${address.slice(-4)}`;
}
