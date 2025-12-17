# syntax=docker/dockerfile:1

FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# copy built frontend assets from node stage
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

RUN chmod +x ./docker-entrypoint.sh ./scripts/start_server.sh

ENV APP_ENV=dev

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["./scripts/start_server.sh"]


