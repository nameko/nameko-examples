HTMLCOV_DIR ?= htmlcov

IMAGES := orders # orders products gateway

# test

coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 orders products gateway
	coverage run -m pytest gateway/test $(ARGS)
	coverage run --append -m pytest orders/test $(ARGS)
	coverage run --append -m pytest products/test $(ARGS)

coverage: test coverage-report coverage-html

# docker

build-example-base:
	docker build --target base -t nameko-example-base -f docker/base.docker .;

build-wheel-builder: build-example-base
	docker build --target build -t nameko-example-builder -f docker/base.docker .;

# run-wheel-builder: build-wheel-builder
# 	for image in $(IMAGES) ; do make -C $$image run-wheel-builder; done

build-images: build-wheel-builder
	for image in $(IMAGES) ; do make -C $$image build-image; done

build: build-images

docker-login:
	docker login --password=$(DOCKER_PASSWORD) --username=$(DOCKER_USERNAME)

push-images: build
	for image in $(IMAGES) ; do make -C $$image push-image; done
