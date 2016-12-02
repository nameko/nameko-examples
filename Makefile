HTMLCOV_DIR ?= htmlcov

IMAGES := orders gateway

# test

coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 orders gateway
	coverage run -m pytest gateway/test $(ARGS)
	coverage run -m pytest orders/test $(ARGS)

coverage: test coverage-report coverage-html

# docker

build-example-base:
	docker build -t nameko-example-base -f docker/docker.base .;

build-wheel-builder: build-example-base
	docker build -t nameko-example-builder -f docker/docker.build .;

run-wheel-builder: build-wheel-builder
	for image in $(IMAGES) ; do make -C $$image run-wheel-builder; done

build-images: run-wheel-builder
	for image in $(IMAGES) ; do make -C $$image build-image; done

build: build-images
