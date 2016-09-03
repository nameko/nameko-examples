# Nameko Examples

[![CircleCI](https://circleci.com/gh/nameko/nameko-examples/tree/orders.svg?style=svg)](https://circleci.com/gh/nameko/nameko-examples/tree/orders)

TODO: Overview of the project

# Prerequisites

* Python 3
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

# Run tests

Ensure RabbitMQ is running.

`$ make coverage`

# Run docker compose

Quickest way to try out examples is to run them with [Docker Compose](https://docs.docker.com/compose/)

`$ docker-compose up`

Docker images for [RabbitMQ](https://hub.docker.com/_/rabbitmq/), [PostgreSQL](https://hub.docker.com/_/postgres/) and [Redis](https://hub.docker.com/_/redis/) will be automatically downloaded and their containers linked to our service containers.
