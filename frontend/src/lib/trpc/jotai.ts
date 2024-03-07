// https://github.com/trpc/trpc/blob/next/packages/client/src/createTRPCClientProxy.ts

import type {
	CreateTRPCClientOptions,
	Resolver,
	TRPCClientError,
	TRPCRequestOptions,
} from "@trpc/client";
import type {
	AnyMutationProcedure,
	AnyProcedure,
	AnyQueryProcedure,
	AnyRootConfig,
	AnyRouter,
	AnySubscriptionProcedure,
	ProcedureArgs,
	ProcedureRouterRecord,
	inferProcedureInput,
	inferProcedureOutput,
} from "@trpc/server";
import type {
	Unsubscribable,
	inferObservableValue,
} from "@trpc/server/observable";
import type { inferTransformedSubscriptionOutput } from "@trpc/server/shared";
import type { Atom, Getter, WritableAtom } from "jotai/vanilla";

import { createTRPCClient } from "@trpc/client";
import { atom } from "jotai/vanilla";
import { atomWithObservable } from "jotai/vanilla/utils";

const getProcedure = (obj: any, path: string[]) => {
	for (let i = 0; i < path.length; ++i) {
		obj = obj[path[i] as string];
	}
	return obj;
};

const isGetter = <T>(v: ((get: Getter) => T) | T): v is (get: Getter) => T =>
	typeof v === "function";

type ValueOrGetter<T> = ((get: Getter) => T) | T;
type AsyncValueOrGetter<T> =
	| ((get: Getter) => Promise<T>)
	| ((get: Getter) => T)
	| Promise<T>
	| T;

export const DISABLED = Symbol();

type CustomOptions = { disabledOutput?: unknown };

const atomWithQuery = <TProcedure extends AnyQueryProcedure, TClient>(
	path: string[],
	getClient: (get: Getter) => TClient,
	getInput: AsyncValueOrGetter<
		inferProcedureInput<TProcedure> | typeof DISABLED
	>,
	getOptions?: ValueOrGetter<TRPCRequestOptions & CustomOptions>
) => {
	type Output = inferProcedureOutput<TProcedure>;
	const queryAtom = atom(async (get, { signal }) => {
		const procedure = getProcedure(getClient(get), path);
		const options = isGetter(getOptions) ? getOptions(get) : getOptions;
		const input = await (isGetter(getInput) ? getInput(get) : getInput);
		if (input === DISABLED) {
			return options?.disabledOutput;
		}
		const output: Output = await procedure.query(input, { signal, ...options });
		return output;
	});
	return queryAtom;
};

const atomWithMutation = <TProcedure extends AnyMutationProcedure, TClient>(
	path: string[],
	getClient: (get: Getter) => TClient
) => {
	type Args = ProcedureArgs<TProcedure["_def"]>;
	type Output = inferProcedureOutput<TProcedure>;
	const mutationAtom = atom(
		null as Output | null,
		async (get, set, args: Args) => {
			const procedure = getProcedure(getClient(get), path);
			const result: Output = await procedure.mutate(...args);
			set(mutationAtom, result);
			return result;
		}
	);
	return mutationAtom;
};

const atomWithSubscription = <
	TProcedure extends AnySubscriptionProcedure,
	TClient
>(
	path: string[],
	getClient: (get: Getter) => TClient,
	getInput: ValueOrGetter<inferProcedureInput<TProcedure>>,
	getOptions?: ValueOrGetter<TRPCRequestOptions>
) => {
	type Output = inferProcedureOutput<TProcedure>;
	const subscriptionAtom = atomWithObservable((get) => {
		const procedure = getProcedure(getClient(get), path);
		const input = isGetter(getInput) ? getInput(get) : getInput;
		const options = isGetter(getOptions) ? getOptions(get) : getOptions;
		const observable = {
			subscribe: (arg: {
				error: (err: unknown) => void;
				next: (result: Output) => void;
			}) => {
				const callbacks = {
					onError: arg.error.bind(arg),
					onNext: arg.next.bind(arg),
				};
				const unsubscribable = procedure.subscribe(input, {
					...options,
					...callbacks,
				});
				return unsubscribable;
			},
		};
		return observable;
	});
	return subscriptionAtom;
};

type QueryResolver<TProcedure extends AnyProcedure, TClient> = {
	(
		getInput: AsyncValueOrGetter<
			ProcedureArgs<TProcedure["_def"]>[0] | typeof DISABLED
		>,
		getOptions?: ValueOrGetter<
			ProcedureArgs<TProcedure["_def"]>[1] & { disabledOutput?: undefined }
		>,
		getClient?: (get: Getter) => TClient
	): Atom<Promise<inferProcedureOutput<TProcedure> | undefined>>;
	(
		getInput: AsyncValueOrGetter<ProcedureArgs<TProcedure["_def"]>[0]>,
		getOptions?: ValueOrGetter<ProcedureArgs<TProcedure["_def"]>[1]>,
		getClient?: (get: Getter) => TClient
	): Atom<Promise<inferProcedureOutput<TProcedure>>>;
	<DisabledOutput>(
		getInput: AsyncValueOrGetter<
			ProcedureArgs<TProcedure["_def"]>[0] | typeof DISABLED
		>,
		getOptions: ValueOrGetter<
			ProcedureArgs<TProcedure["_def"]>[1] & { disabledOutput: DisabledOutput }
		>,
		getClient?: (get: Getter) => TClient
	): Atom<Promise<DisabledOutput | inferProcedureOutput<TProcedure>>>;
};

type MutationResolver<TProcedure extends AnyProcedure, TClient> = (
	getClient?: (get: Getter) => TClient
) => WritableAtom<
	inferProcedureOutput<TProcedure> | null,
	[ProcedureArgs<TProcedure["_def"]>],
	Promise<inferProcedureOutput<TProcedure>>
>;

type SubscriptionResolver<TProcedure extends AnyProcedure, TClient> = (
	getInput: ValueOrGetter<ProcedureArgs<TProcedure["_def"]>[0]>,
	getOptions?: ValueOrGetter<ProcedureArgs<TProcedure["_def"]>[1]>,
	getClient?: (get: Getter) => TClient
) => Atom<inferObservableValue<inferProcedureOutput<TProcedure>>>;

interface TRPCSubscriptionObserver<TValue, TError> {
	onComplete: () => void;
	onData: (value: TValue) => void;
	onError: (err: TError) => void;
	onStarted: () => void;
	onStopped: () => void;
}
type NativeSubscriptionResolver<
	TConfig extends AnyRootConfig,
	TProcedure extends AnyProcedure
> = (
	...args: [
		input: ProcedureArgs<TProcedure["_def"]>[0],
		opts: Partial<
			TRPCSubscriptionObserver<
				inferTransformedSubscriptionOutput<TConfig, TProcedure>,
				TRPCClientError<TConfig>
			>
		> &
			ProcedureArgs<TProcedure["_def"]>[1]
	]
) => Unsubscribable;

type DecorateProcedure<
	TConfig extends AnyRootConfig,
	TProcedure extends AnyProcedure,
	TClient
> = TProcedure extends AnyQueryProcedure
	? {
			atomWithQuery: QueryResolver<TProcedure, TClient>;
			query: Resolver<TConfig, TProcedure>;
	  }
	: TProcedure extends AnyMutationProcedure
	? {
			atomWithMutation: MutationResolver<TProcedure, TClient>;
			mutate: Resolver<TConfig, TProcedure>;
	  }
	: TProcedure extends AnySubscriptionProcedure
	? {
			atomWithSubscription: SubscriptionResolver<TProcedure, TClient>;
			subscribe: NativeSubscriptionResolver<TConfig, TProcedure>;
	  }
	: never;

type DecoratedProcedureRecord<
	TRouter extends AnyRouter,
	TProcedures extends ProcedureRouterRecord,
	TClient
> = {
	[TKey in keyof TProcedures]: TProcedures[TKey] extends AnyRouter
		? DecoratedProcedureRecord<
				TRouter,
				TProcedures[TKey]["_def"]["record"],
				TClient
		  >
		: TProcedures[TKey] extends AnyProcedure
		? DecorateProcedure<TRouter["_def"]["_config"], TProcedures[TKey], TClient>
		: never;
};

export function createTRPCJotai<TRouter extends AnyRouter>(
	opts: CreateTRPCClientOptions<TRouter>
) {
	const client = createTRPCClient<TRouter>(opts);

	const createProxy = (target: any, path: readonly string[] = []): any => {
		return new Proxy(
			() => {
				// empty
			},
			{
				apply(_target, _thisArg, args) {
					const parentProp = path[path.length - 1];
					const parentPath = path.slice(0, -1);
					if (parentProp === "atomWithQuery") {
						const [getInput, getOptions, getClient] = args;
						return atomWithQuery(
							parentPath,
							getClient || (() => client),
							getInput,
							getOptions
						);
					}
					if (parentProp === "atomWithMutation") {
						const [getClient] = args;
						return atomWithMutation(parentPath, getClient || (() => client));
					}
					if (parentProp === "atomWithSubscription") {
						const [getInput, getOptions, getClient] = args;
						return atomWithSubscription(
							parentPath,
							getClient || (() => client),
							getInput,
							getOptions
						);
					}

					// console.log({ parentProp, parentPath, args });
					return target(...args);
					// throw new Error(`unexpected function call ${path.join("/")}`);
				},
				get(_target, prop: string) {
					return createProxy(target[prop], [...path, prop]);
				},
			}
		);
	};

	return createProxy(client) as DecoratedProcedureRecord<
		TRouter,
		TRouter["_def"]["record"],
		typeof client
	>;
}
