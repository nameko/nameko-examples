#!/bin/bash

# Check if rabbit is up and running before starting the service.

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

# Run Service

nameko run --config config.yml gateway.service --backdoor 3000
