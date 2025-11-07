#!/bin/sh
set -e

APP_PORT="${PORT:-8000}"

echo "[start_server] Starting uvicorn on port ${APP_PORT}"
exec uvicorn api.main:app --host 0.0.0.0 --port "${APP_PORT}" --log-level info

