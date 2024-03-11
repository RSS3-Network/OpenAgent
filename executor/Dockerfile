FROM node:18

RUN npm install -g pnpm

WORKDIR /app

COPY package.json ./
COPY pnpm-lock.yaml ./
COPY tsconfig*.json ./

RUN pnpm install --frozen-lockfile

COPY ./src ./src
COPY ./test ./test
COPY ./prisma ./prisma

RUN pnpm run build
RUN pnpm prisma generate

EXPOSE 3333

CMD ["pnpm", "run", "start:prod"]
