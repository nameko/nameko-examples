TAG ?= dev

# docker

build-image:
	docker build -t nameko/nameko-example-gateway:$(TAG) .;

push-image:
	docker push nameko/nameko-example-gateway:$(TAG)
