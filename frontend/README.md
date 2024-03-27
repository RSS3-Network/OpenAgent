# OpenAgent Frontend

## Development

### 1. Install Dependencies

```bash
pnpm install
```

### 2. Setup the Database

Start the postgres database in docker locally:

```bash
pnpm run docker:db
```

Migrate the local database:

```bash
pnpm run prisma:migrate:dev
```

### 3. Complete the environment variables

Copy the `.env.example` file to `.env.local` and fill in the environment variables.

#### 3.1. Auth

The authentication is done with [Auth.js](https://authjs.dev/). The following environment variables are required to let users sign in with their Google, Discord, and email accounts.

```bash
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="random-secret-for-dev"
AUTH_GOOGLE_CLIENT_ID=""
AUTH_GOOGLE_CLIENT_SECRET=""
AUTH_GMAIL_USER=""
AUTH_GMAIL_PASS=""
AUTH_DISCORD_CLIENT_ID=""
AUTH_DISCORD_CLIENT_SECRET=""
```

You can refer to the [Auth.js documentation](https://authjs.dev/) for more information. For example, the [Google Provider](https://authjs.dev/reference/core/providers/google#resources).

#### 3.2. Database

The database is managed with [Prisma](https://www.prisma.io/). The following environment variables are required to connect to the database.

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=openagent
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=public
```

These environment variables are used in the `prisma/schema.prisma` file to connect to the database. It's set by default in `.env.example`, update the values according to your environment.

#### 3.3 Backend API

The backend API is used to fetch data from server. The following environment variables are required to connect to the backend API.

```bash
BACKEND_URL="https://YOUR_BACKEND_URL"
API_EXECUTOR_URL="https://YOUR_API_EXECUTOR_URL"
```

#### 3.4 Wallet

The wallet is used to sign transactions and interact with the blockchain. The following environment variables are required to connect to the wallet.

```bash
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=
NEXT_PUBLIC_CHAIN_ID=
```

Note: For `NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID`, every dApp that relies on WalletConnect now needs to obtain a projectId from [WalletConnect Cloud](https://cloud.walletconnect.com/sign-in). This is absolutely free and only takes a few minutes.

For `NEXT_PUBLIC_CHAIN_ID`, you can refer to the [Chainlist](https://www.chainlist.org/) for the chain ID of the blockchain you want to connect to. For example, in production, it should be `1` for mainnet; and in development, it could be `11155111` for Sepolia testnet.

### 4. Run the Development Server

Run the development server:

```bash
pnpm run dev
```

The frontend is running at [http://localhost:3000](http://localhost:3000).

The framework used is [Next.js](https://nextjs.org/). You can refer to the [documentation](https://nextjs.org/docs) for more information.

## Deployment

You can deploy the frontend to Vercel, Netlify, or any other platforms that support Next.js. a Dockerfile is also provided for your reference.

Before deploying, you may want to complete the environment variables in the `.env.production` file and set up the deployment configuration.
