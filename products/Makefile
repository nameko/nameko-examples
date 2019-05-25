build-image:
	docker build -t nameko/nameko-example-products:$(TAG) .;

docker-tag:
	docker tag nameko/nameko-example-products:$(FROM_TAG) \
	nameko/nameko-example-products:$(TAG)

push-image:
	docker push nameko/nameko-example-products:$(TAG)
