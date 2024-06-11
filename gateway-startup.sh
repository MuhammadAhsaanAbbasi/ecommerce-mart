#!/bin/sh

# Check if .env file exists and load environment variables
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

# Define Kong admin URL
KONG_ADMIN_URL="http://localhost:8001"
ADMIN_SECRET_KEY="d1da7ff1395c4a15b7b3601ba2676200"
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
    --data "paths[]=/user-service" \
    --data "strip_path=true"

# Service: product-service
curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=product-service" \
    --data "url=http://host.docker.internal:8082"

curl -i -X POST $KONG_ADMIN_URL/services/product-service/plugins \
    --data "name=jwt"

curl -i -X POST $KONG_ADMIN_URL/services/product-service/routes \
    --data "paths[]=/product-service" \
    --data "strip_path=true"

# Service: order-service
curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=order-service" \
    --data "url=http://host.docker.internal:8083"

curl -i -X POST $KONG_ADMIN_URL/services/order-service/plugins \
    --data "name=jwt"

curl -i -X POST $KONG_ADMIN_URL/services/order-service/routes \
    --data "paths[]=/order-service" \
    --data "strip_path=true"

# Service: inventory-service
curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=inventory-service" \
    --data "url=http://host.docker.internal:8084"

curl -i -X POST $KONG_ADMIN_URL/services/inventory-service/plugins \
    --data "name=jwt" \

curl -i -X POST $KONG_ADMIN_URL/services/inventory-service/routes \
    --data "paths[]=/inventory-service" \
    --data "strip_path=true"

# Service: payment-service
curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=payment-service" \
    --data "url=http://host.docker.internal:8085"

curl -i -X POST $KONG_ADMIN_URL/services/payment-service/plugins \
    --data "name=jwt"

curl -i -X POST $KONG_ADMIN_URL/services/payment-service/routes \
    --data "paths[]=/payment-service" \
    --data "strip_path=true"

# Service: notification-service
curl -i -X POST $KONG_ADMIN_URL/services/ \
    --data "name=notification-services" \
    --data "url=http://host.docker.internal:8086"

curl -i -X POST $KONG_ADMIN_URL/services/notification-services/plugins \
    --data "name=jwt"

curl -i -X POST $KONG_ADMIN_URL/services/notification-services/routes \
    --data "paths[]=/notification-services" \
    --data "strip_path=true"

# Register admin consumer
curl -i -X POST $KONG_ADMIN_URL/consumers/ \
    --data "username=mahsaanabbasi@gmail.com" \
    --data "custom_id=123"

curl -i -X POST $KONG_ADMIN_URL/consumers/mahsaanabbasi@gmail.com/jwt \
    --data "key=$ADMIN_SECRET_KEY"