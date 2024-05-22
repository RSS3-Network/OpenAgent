# Install dependencies only when needed
FROM node:20.1.0-alpine AS deps

# Install dependencies for node-gyp
RUN apk update && apk add --no-cache \
    make g++ py3-pip

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json ./
COPY pnpm-lock.yaml ./
COPY prisma ./prisma
RUN corepack pnpm install --frozen-lockfile

# Rebuild the source code only when needed
FROM node:20.1.0-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable the usage data collection of Next.js.
ENV NEXT_TELEMETRY_DISABLED 1

# Copy env variables
COPY .env.ci .env

# RUN apk add --no-cache git
RUN npx next telemetry disable
RUN npm run build

# Production image, copy all the files and run next
FROM node:20-alpine AS runner
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED 1

# Don't run as root
# RUN addgroup --system --gid 1001 nodejs
# RUN adduser --system --uid 1001 nextjs
# USER nextjs

COPY --from=builder --chown=nextjs:nodejs /app/ ./

# RUN apt-get update -y && apt-get install -y openssl

EXPOSE 3000

ENV PORT 3000
