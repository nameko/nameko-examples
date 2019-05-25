#!/bin/bash

# Check if rabbit and redis are up and running before starting the service.

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "$(date) - waiting for redis..."
    sleep 2
done

# Run the service

nameko run --config config.yml products.service --backdoor 3000
