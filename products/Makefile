# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		nameko-example-builder;

build-image:
	docker build -t nameko/nameko-example-products:latest -f docker.run .;
