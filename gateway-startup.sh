#!/bin/sh

# Check if .env file exists and load environment variables
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

# Define Kong admin URL
KONG_ADMIN_URL="http://localhost:8001"

# Wait for Kong to be ready
until curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL; do
    printf '.'
    sleep 5
done

# Register services and add JWT plugin to each service
# Service: user-service
curl -i -X POST $KONG_ADMIN_URL/services \
    --data "name=user-service" \
    --data "url=http://host.docker.internal:8081"

curl -i -X POST $KONG_ADMIN_URL/services/user-service/routes \
    --data "paths[]=user-service" \
    --data "strip_path=true" \