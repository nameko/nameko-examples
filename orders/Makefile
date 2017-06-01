TAG ?= dev
# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		nameko-example-builder;

build-image:
	docker build -t nameko/nameko-example-orders:latest -f docker.run .;

tag-image:
	docker tag nameko/nameko-example-orders:latest nameko/nameko-example-orders:$(TAG)

push-image: tag-image
	docker push nameko/nameko-example-orders:$(TAG)
