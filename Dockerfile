# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./docker-entrypoint.sh ./scripts/start_server.sh

ENV APP_ENV=dev

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["./scripts/start_server.sh"]


