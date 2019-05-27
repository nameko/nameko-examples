FROM nameko-example-builder AS wheels

COPY . /application

RUN cd /application && pip wheel .

# ------------------------------------------------------------------------

FROM nameko-example-base AS install

COPY --from=wheels /application/wheelhouse /wheelhouse

RUN pip install --no-index -f /wheelhouse nameko_examples_gateway

# ------------------------------------------------------------------------

FROM nameko-example-base

COPY --from=install /appenv /appenv

COPY config.yml /var/nameko/config.yml
COPY run.sh /var/nameko/run.sh

RUN chmod +x /var/nameko/run.sh

USER nameko

WORKDIR /var/nameko/

EXPOSE 8000

CMD /var/nameko/run.sh;
