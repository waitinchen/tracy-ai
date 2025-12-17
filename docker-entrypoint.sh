#!/bin/sh
set -e

# Determine which env file to load. Priority:
# 1. ENV_FILE environment variable (absolute path)
# 2. config/.env.<APP_ENV>
# 3. Existing /app/.env (if already mounted)

TARGET_ENV_FILE="${ENV_FILE:-}" 

if [ -z "$TARGET_ENV_FILE" ]; then
  APP_ENV_NAME="${APP_ENV:-dev}"
  TARGET_ENV_FILE="/app/config/.env.${APP_ENV_NAME}"
fi

if [ -f "$TARGET_ENV_FILE" ]; then
  echo "[entrypoint] Loading environment from $TARGET_ENV_FILE"
  cp "$TARGET_ENV_FILE" /app/.env
elif [ -f /app/.env ]; then
  echo "[entrypoint] Using existing /app/.env"
else
  echo "[entrypoint] Warning: no environment file found (expected $TARGET_ENV_FILE)."
fi

exec "$@"


