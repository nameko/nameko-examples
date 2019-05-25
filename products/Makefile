TAG ?= dev
# docker

build-image:
	docker build -t nameko/nameko-example-products:$(TAG) .;

push-image:
	docker push nameko/nameko-example-products:$(TAG)
