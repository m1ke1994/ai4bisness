FROM node:20-alpine AS dependencies
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS build
WORKDIR /app

COPY --from=dependencies /app/node_modules ./node_modules
COPY package.json package-lock.json ./
COPY app.vue nuxt.config.ts tailwind.config.js ./
COPY assets ./assets
COPY components ./components
COPY composables ./composables
COPY data ./data
COPY layouts ./layouts
COPY pages ./pages
COPY plugins ./plugins
COPY public ./public

RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app

ENV NODE_ENV=production
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=3000

COPY --from=build /app/.output ./.output

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
