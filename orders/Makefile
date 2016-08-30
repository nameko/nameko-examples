# docker

run:
	docker run -it -d -p 8001:8000 \
	--link rabbit:rabbit --link postgres:postgres \
	--net namekoexamples_default \
	--name orders nameko/nameko-example-orders:latest

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		nameko-example-builder;

build-image:
	docker build -t nameko/nameko-example-orders:latest -f docker.run .;
