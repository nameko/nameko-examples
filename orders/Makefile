TAG ?= dev
# docker

build-image:
	docker build -t nameko/nameko-example-orders:$(TAG) .;

push-image:
	docker push nameko/nameko-example-orders:$(TAG)
