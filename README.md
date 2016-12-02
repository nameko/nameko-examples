# Nameko Examples

[![CircleCI](https://circleci.com/gh/nameko/nameko-examples/tree/master.svg?style=svg)](https://circleci.com/gh/nameko/nameko-examples/tree/master)

## Prerequisites

* [Python 3](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

## Overview

### Repository structure
When developing Nameko services you have a freedom to organize your repo structure anyway you want.

For this example we placed 3 Nameko services: `Products`, `Orders` and `Gateway` in one repository.

While possible, this is not necessarily the best practice. Aim to apply Domain Driven Design concepts and try to place only services that belong to the same bounded context in one repository e.g., Product (main service responsible for serving products) and Product Indexer (a service responsible for listening for product change events and indexing product data within search database).

### Services
#### Products Service

Responsible for storing and managing product information and exposing RPC Api that can be consumed by other services. This service is using Redis as it's data store. Example includes implementation of Nameko's [DependencyProvider](https://nameko.readthedocs.io/en/stable/key_concepts.html#dependency-injection) `Storage` which is used for talking to Redis.

#### Orders Service

Responsible for storing and managing orders information and exposing RPC Api that can be consumed by other services.

This service is using MySQL database to persist order information.
- [nameko-sqlalchemy](https://pypi.python.org/pypi/nameko-sqlalchemy)  dependency is used to expose [SQLAlchemy](http://www.sqlalchemy.org/) session to the service class.
- [Alembic](https://pypi.python.org/pypi/alembic) is used for database migrations.

#### Gateway Service

Is a service exposing HTTP Api to be used by external clients e.g., Web and Mobile APPS. It coordinates all incoming requests and composes responses based on data from underlying domain services.

[Marshmallow](https://pypi.python.org/pypi/marshmallow) is used for validating, serializing and deserializing complex Python objects to JSON and vice versa in all services.

## Run examples

Quickest way to try out examples is to run them with Docker Compose

`$ docker-compose up`

Docker images for [RabbitMQ](https://hub.docker.com/_/rabbitmq/), [PostgreSQL](https://hub.docker.com/_/postgres/) and [Redis](https://hub.docker.com/_/redis/) will be automatically downloaded and their containers linked to example service containers.

## Run tests

Ensure RabbitMQ, MySQL and Redis are running and `config.yaml` files for each service are configured correctly. 

`$ make coverage`
