build-image:
	docker build -t nameko/nameko-example-orders:$(TAG) .;

docker-tag:
	docker tag nameko/nameko-example-orders:$(FROM_TAG) \
	nameko/nameko-example-orders:$(TAG)

push-image:
	docker push nameko/nameko-example-orders:$(TAG)
