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

These environment variables are used in the `prisma/schema.prisma` file to connect to the database. It's set by default in `.env.example` file to align with the `docker-compose.yml` file. You may need to change it if you are using a different database or deployment.

#### 3.3 Backend API

The backend API is used to fetch data from server. The following environment variables are required to connect to the backend API.

```bash
API_AI_URL="https://YOUR_API_AI_URL"
API_EXECUTOR_URL="https://YOUR_API_EXECUTOR_URL"
```

### 4. Run the Development Server

Run the development server:

```bash
pnpm run dev
```

The frontend is running at [http://localhost:3000](http://localhost:3000).

The framework used is [Next.js](https://nextjs.org/). You can refer to the [documentation](https://nextjs.org/docs) for more information.

## Deployment

You can deploy the frontend to Vercel, Netlify, or any other platforms that support Next.js. Also, a Dockerfile is provided to build a Docker image and deploy it to a container platform.

Before deploying, you may want to complete the environment variables in the `.env.production` file and set up the deployment configuration.
