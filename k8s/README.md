# Run Nameko Examples on Kubernetes

![Nameko loves Kubernetes](nameko-k8s.png)

In this example we'll use local Kubernetes cluster installed with [docker-for-desktop](https://docs.docker.com/docker-for-mac/)
 along with community maintained Helm Charts to deploy all 3rd party services. 
 We will also create a set of Helm Charts for Nameko Example Services from this repository.  

Tested with Kubernetes v1.14.8

## Prerequisites

Please make sure these are installed and working

* [docker-for-desktop](https://docs.docker.com/docker-for-mac/) with Kubernetes enabled. Docker Desktop for Mac is used in these examples but any other Kubernetes cluster will work as well.
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) - should be installed and configured during docker-for-desktop installation
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)

Verify our Kubernetes cluster us up and running:

```sh
$ kubectl --context=docker-desktop get nodes

NAME             STATUS   ROLES    AGE   VERSION
docker-desktop   Ready    master   54m   v1.14.8
```

## Create Namespace

It's a good practice to create a namespaces where all of our services will live:

```yaml
# namespace.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: examples
```

```sh
$ kubectl --context=docker-desktop apply -f namespace.yaml

namespace/examples created
```

## Install External Dependencies

Our examples depend on PostgreSQL, Redis and RabbitMQ. 
The fastest way to install these 3rd party dependencies is to use community maintained [Helm Charts](https://github.com/kubernetes/charts).

Let's verify that Helm client is installed

```sh
$ helm version --kube-context=docker-desktop

version.BuildInfo{Version:"v3.0.0", GitCommit:"e29...8b6", GitTreeState:"clean", GoVersion:"go1.13.4"}
```

### Deploy RabbitMQ, PostgreSQL and Redis

Run these commands one by one:

```sh
$ helm --kube-context=docker-desktop install broker  --namespace examples stable/rabbitmq

$ helm --kube-context=docker-desktop install db --namespace examples stable/postgresql --set postgresqlDatabase=orders

$ helm --kube-context=docker-desktop install cache  --namespace examples stable/redis
```

RabbitMQ, PostgreSQL and Redis are now installed along with persistent volumes, kubernetes services, config maps and any secrets required a.k.a. `Amazing™`!

Verify all pods are running:

```sh
$ kubectl --context=docker-desktop --namespace=examples get pods

NAME                               READY     STATUS    RESTARTS   AGE
broker-rabbitmq-0                   1/1       Running   0          49s
cache-redis-master-0                1/1       Running   0          49s
cache-redis-slave-79fc9cc57-s52gw   1/1       Running   0          49s
db-postgresql-0                     1/1       Running   0          49s
```

## Deploy Example Services

To deploy our example services, we'll have to create Kubernetes deployment definition files. 
Most of the time (in real world) you would want to use some dynamic data during your deployments e.g. define image tags.
The easiest way to do this is to create Helm Charts for each of our service and use Helm to deploy them. 

Our charts are organized as follows:

```txt
charts
├── gateway
│   ├── Chart.yaml
│   ├── templates
│   │   ├── NOTES.txt
│   │   ├── deployment.yaml
│   │   ├── ingress.yaml
│   │   └── service.yaml
│   └── values.yaml
├── orders
│   ├── Chart.yaml
│   ├── templates
│   │   ├── NOTES.txt
│   │   └── deployment.yaml
│   └── values.yaml
└── products
    ├── Chart.yaml
    ├── templates
    │   ├── NOTES.txt
    │   └── deployment.yaml
    └── values.yaml
```

Each chart is comprised of:

`Charts.yaml` file containing description of the chart.  
`values.yaml` file containing default values for a chart that can be overwritten during the release..  
`templates` folder where all Kubernetes definition files live.

All of our charts contain `deployment.yaml` template where main Nameko Service deployment definition lives. `Gateway` chart has additional definitions for `ingress` and kubernetes `service` which are required to enable inbound traffic.

Example of products `deployment.yaml`:

```yaml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
  labels:
    app: {{ .Chart.Name }}
    tag: {{ .Values.image.tag }}
    revision: "{{ .Release.Revision }}"
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
      - image: nameko/nameko-example-products:{{ .Values.image.tag }}
        name: {{ .Chart.Name }}
        env:
          - name: REDIS_HOST
            value: cache-redis-master
          - name: REDIS_INDEX
            value: "11"
          - name: REDIS_PORT
            value: "6379"
          - name: REDIS_PASSWORD
            valueFrom:
              secretKeyRef:
                name: cache-redis
                key: redis-password
          - name: RABBIT_HOST
            value: broker-rabbitmq
          - name: RABBIT_MANAGEMENT_PORT
            value: "15672"
          - name: RABBIT_PORT
            value: "5672"
          - name: RABBIT_USER
            value: user
          - name: RABBIT_PASSWORD
            valueFrom:
              secretKeyRef:
                name: broker-rabbitmq
                key: rabbitmq-password
      restartPolicy: Always

```

As you can see this template is using values coming from `Chart` and `Values` files as well as dynamic `Release` information. Passwords from secrets created by Redis and RabbitMQ releases are also referenced and passed to a container as `REDIS_PASSWORD` and `RABBIT_PASSWORD` environment variables respectively.

Please read [The Chart Template Developer’s Guide](https://docs.helm.sh/chart_template_guide/#the-chart-template-developer-s-guide)
to learn about creating your own charts.

To route traffic to our gateway service we'll be using ingress. For ingress to work `Ingress Controller` has to be enabled on our cluster. Follow instructions form [Ingress Installation docs](https://kubernetes.github.io/ingress-nginx/deploy/):

```sh
$ kubectl --context=docker-desktop apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml

$ kubectl --context=docker-desktop apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud-generic.yaml
```

Let's deploy our `products` chart:

```sh
$ helm upgrade products charts/products --install \
	--namespace=examples --kube-context=docker-desktop \
	--set image.tag=latest

Release "products" does not exist. Installing it now.
NAME:   products
LAST DEPLOYED: Thu Jan 11 17:08:51 2018
NAMESPACE: examples
STATUS: DEPLOYED

RESOURCES:
==> v1beta2/Deployment
NAME      DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
products  1        1        1           0          0s


NOTES:
Thank you for installing Products Service!
```

We used `--set image.tag=latest` to set custom image tag to be used for this release. You can do the same for any values defined in values.yaml file.

Let's release `orders` and `gateway` services:

```sh
$ helm upgrade orders charts/orders --install \
	--namespace=examples --kube-context=docker-desktop \
	--set image.tag=latest

Release "orders" does not exist. Installing it now.
(...)

$ helm upgrade gateway charts/gateway --install \
	--namespace=examples --kube-context=docker-desktop \
	--set image.tag=latest

Release "gateway" does not exist. Installing it now.
(...)
```

Let's list all of our Helm releases:

```sh
$ helm --kube-context=docker-desktop list --namespace examples

NAME    	REVISION	UPDATED                 	STATUS  	CHART
broker  	1       	Tue Oct 29 06:50:26 2019	DEPLOYED	rabbitmq-4.11.1
cache   	1       	Tue Oct 29 06:50:43 2019	DEPLOYED	redis-6.4.4
db      	1       	Tue Oct 29 06:50:35 2019	DEPLOYED	postgresql-3.16.1
gateway 	1       	Tue Oct 29 06:54:09 2019	DEPLOYED	gateway-0.1.0
orders  	1       	Tue Oct 29 06:54:01 2019	DEPLOYED	orders-0.1.0
products	1       	Tue Oct 29 06:53:43 2019	DEPLOYED	products-0.1.0
```

And again let's verify pods are happily running:

```sh
$ kubectl --context=docker-desktop --namespace=examples get pods

NAME                                 READY   STATUS    RESTARTS   AGE
broker-rabbitmq-0                    1/1     Running   0          6m30s
cache-redis-master-0                 1/1     Running   0          6m13s
cache-redis-slave-0                  1/1     Running   0          6m13s
db-postgresql-0                      1/1     Running   0          6m20s
gateway-65d67f5dd4-kfbxq             1/1     Running   0          2m47s
orders-5c6d788d79-d4f8c              1/1     Running   0          2m55s
products-55bbcf7894-ff5lz            1/1     Running   0          3m13s
```

## Run examples

We can now verify our gateway api is working as expected by executing sample requests found in main README of this repository.

#### Create Product

```sh
$ curl -XPOST -d '{"id": "the_odyssey", "title": "The Odyssey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}' 'http://localhost/products'

{"id": "the_odyssey"}
```

#### Get Product

```sh
$ curl 'http://localhost/products/the_odyssey'

{
  "id": "the_odyssey",
  "title": "The Odyssey",
  "passenger_capacity": 101,
  "maximum_speed": 5,
  "in_stock": 10
}
```
#### Create Order

```sh
$ curl -XPOST -d '{"order_details": [{"product_id": "the_odyssey", "price": "100000.99", "quantity": 1}]}' 'http://localhost/orders'

{"id": 1}
```

#### Get Order

```sh
$ curl 'http://localhost/orders/1'

{
  "id": 1,
  "order_details": [
    {
      "id": 1,
      "quantity": 1,
      "product_id": "the_odyssey",
      "image": "http://www.example.com/airship/images/the_odyssey.jpg",
      "price": "100000.99",
      "product": {
        "maximum_speed": 5,
        "id": "the_odyssey",
        "title": "The Odyssey",
        "passenger_capacity": 101,
        "in_stock": 9
      }
    }
  ]
}
```

## Wrap-up

Running Nameko services in Kubernetes is really simple. Please get familiar with Helm Charts included in this repository and try adding one of your own. 
