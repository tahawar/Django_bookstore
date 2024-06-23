#!/usr/bin/env bash
# wait-for-it.sh

host="$1"
shift
port="$1"
shift

until nc -z "$host" "$port"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"
