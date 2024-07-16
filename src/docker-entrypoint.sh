#!/bin/bash

set -e

echo "run migrations"
alembic upgrade head

echo "run server"

exec python main.py
