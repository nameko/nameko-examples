#!/bin/bash

is_ready() {
    # TODO: Use creds from env vars.
    eval "curl -I $RABBIT_USER:$RABBIT_PASSWORD http://rabbit:15672/api/vhosts"
}

i=0
while ! is_ready; do
    i=`expr $i + 1`
    if [ $i -ge 10 ]; then
        echo "$(date) - rabbit still not ready, giving up"
        exit 1
    fi
    echo "$(date) - waiting for rabbit to be ready"
    sleep 3
done

nameko run --config config.yml service --backdoor 3000
