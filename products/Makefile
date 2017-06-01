TAG ?= dev
# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		nameko-example-builder;

build-image:
	docker build -t nameko/nameko-example-products:latest -f docker.run .;

tag-image:
	docker tag nameko/nameko-example-products:latest nameko/nameko-example-products:$(TAG)

push-image: tag-image
	docker push nameko/nameko-example-products:$(TAG)
