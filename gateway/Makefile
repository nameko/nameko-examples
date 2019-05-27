build-image:
	docker build -t nameko/nameko-example-gateway:$(TAG) .;

docker-tag:
	docker tag nameko/nameko-example-gateway:$(FROM_TAG) \
	nameko/nameko-example-gateway:$(TAG)

push-image:
	docker push nameko/nameko-example-gateway:$(TAG)
