TAG ?= dev

# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		nameko-example-builder;

build-image:
	docker build -t nameko/nameko-example-gateway:latest -f docker.run .;

tag-image:
	docker tag nameko/nameko-example-gateway:latest nameko/nameko-example-gateway:$(TAG)

push-image: build-image tag-image
	docker push nameko/nameko-example-gateway:$(TAG)
