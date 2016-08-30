IMAGES := orders


# test

coverage-html:
	coverage html --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 orders
	coverage run -m pytest */test $(ARGS)

coverage: test coverage-report coverage-html

# docker

build-example-base:
	docker build -t nameko-example-base -f docker/docker.base .;

build-wheel-builder: build-example-base
	docker build -t nameko-example-builder -f docker/docker.build .;

run-wheel-builder: build-wheel-builder
	for image in $(IMAGES) ; do make -C $$image run-wheel-builder; done

#build-image-base: run-wheel-builder
#	docker build -t nameko-example-base \
#	-f docker/docker.run .;

build-images: run-wheel-builder
	for image in $(IMAGES) ; do make -C $$image build-image; done

build: build-images
