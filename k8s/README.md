# Run Nameko Examples on Kubernetes

![Nameko loves Kubernetes](nameko-k8s.png)

In this example we'll use local [minikube](https://github.com/kubernetes/minikube)
Kubernetes cluster hosted on VirtualBox along with community maintained Helm Charts to deploy all 3rd party services. We will also create a set of Helm Charts for Nameko Example Services from this repository.  

Tested with Kubernetes v1.8.

## Prerequisites

Please make sure these are installed and working

* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)

## Create Kubernetes Cluster

Start (create) Minikube:

```sh
$ minikube start --vm-driver=virtualbox

Starting local Kubernetes v1.8.0 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
Loading cached images from config file.
```

Verify cluster:

```sh
$ kubectl --context=minikube get nodes

NAME       STATUS    ROLES     AGE       VERSION
minikube   Ready     <none>    3m        v1.8.0
```

Minikube comes with Kubernetes Dashboard addon turned on. You can use it to poke around the cluster. Any information that you can see via dashboard can be as easily obtained with `kubectl` command.  

Start dashboard:  
`$ minikube dashboard`

## Create Namespace

It’s a good practice to create a namespaces where all of our services will live:

```yaml
# namespace.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: examples
```

`$ kubectl --context=minikube apply -f namespace.yaml`

## Install External Dependencies

Our examples depend on PostgreSQL, Redis and RabbitMQ. 
The fastest way to install these 3rd party dependencies is to use community maintained [Helm Charts](https://github.com/kubernetes/charts).

Let’s install `Tiller` (Helm’s server-side component)

```sh
$ helm init --kube-context=minikube

$HELM_HOME has been configured at /Users/bob/.helm.

Tiller (the Helm server-side component) has been installed into your Kubernetes Cluster.
Happy Helming!
```

Let’s verify that Helm client can talk to Tiller server

```sh
$ helm version --kube-context=minikube

Client: &version.Version{SemVer:"v2.7.0", GitCommit:"08c...ba4", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.7.0", GitCommit:"08c...ba4", GitTreeState:"clean"}
```

### Deploy RabbitMQ, PostgreSQL and Redis

Run these commands one by one:

```sh
$ helm --kube-context=minikube install --name broker  --namespace examples stable/rabbitmq

$ helm --kube-context=minikube install --name db --namespace examples stable/postgresql --set postgresDatabase=orders

$ helm --kube-context=minikube install --name cache  --namespace examples stable/redis
```

RabbitMQ, PostgreSQL and Redis are now installed along with persistent volumes, kubernetes services, config maps and any secrets required a.k.a. `Amazing™`!

Verify all pods are running:

```sh
$ kubectl --context=minikube --namespace=examples get pods

NAME                               READY     STATUS    RESTARTS   AGE
broker-rabbitmq-6c8d7c4554-8nklq   1/1       Running   0          22m
cache-redis-6cbfd95f66-vlkn5       1/1       Running   0          22m
db-postgresql-67f5c64dc4-8s9vf     1/1       Running   0          49s
```

There is a known bug with minikube version: v0.24.1 and bounding persistent volumes.
If this has not been addressed when you read this please follow [these steps](https://github.com/kubernetes/minikube/issues/2256#issuecomment-355365620) to fix it.

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
            value: cache-redis
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

To route traffic to our gateway service we’ll be using ingress. For ingress to work `Ingress Controller` has to be enabled on our cluster:

`$ minikube addons enable ingress`

Let's deploy our `products` chart:

```sh
$ helm upgrade products charts/products --install \
	--namespace=examples --kube-context=minikube \
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
	--namespace=examples --kube-context=minikube \
	--set image.tag=latest

Release "orders" does not exist. Installing it now.
(...)

$ helm upgrade gateway charts/gateway --install \
	--namespace=examples --kube-context=minikube \
	--set image.tag=latest

Release "gateway" does not exist. Installing it now.
(...)
```

Let's list all of our Helm releases:

```sh
$ helm --kube-context=minikube list

NAME    	REVISION	UPDATED                 	STATUS  	CHART           	NAMESPACE
broker  	1       	Thu Jan 11 16:29:15 2018	DEPLOYED	rabbitmq-0.5.3  	examples
cache   	1       	Thu Jan 11 16:29:27 2018	DEPLOYED	redis-0.7.1     	examples
db      	1       	Thu Jan 11 16:51:05 2018	DEPLOYED	postgresql-0.7.1	examples
gateway 	1       	Thu Jan 11 17:11:52 2018	DEPLOYED	gateway-0.1.0   	examples
orders  	1       	Thu Jan 11 17:11:37 2018	DEPLOYED	orders-0.1.0    	examples
products	1       	Thu Jan 11 17:08:51 2018	DEPLOYED	products-0.1.0  	examples
```

And again let's verify pods are happily running:

```sh
$ kubectl --context=minikube --namespace=examples get pods

NAME                               READY     STATUS    RESTARTS   AGE
broker-rabbitmq-6c8d7c4554-8nklq   1/1       Running   0          22m
cache-redis-6cbfd95f66-vlkn5       1/1       Running   0          22m
db-postgresql-67f5c64dc4-8s9vf     1/1       Running   0          49s
gateway-cbdff8cf-p5p7m             1/1       Running   0          1m
orders-7995b49c59-lcwmm            1/1       Running   0          2m
products-66894ff474-5dd2t          1/1       Running   0          5m
```

## Run examples

We can now verify our gateway api is working as expected by executing sample requests found in main README of this repository.

We will replace `localhost:8003` with minikube IP:

```sh
$ minikube ip
192.168.99.101
```

#### Create Product

```sh
$ curl -XPOST -d '{"id": "the_odyssey", "title": "The Odyssey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}' 'http://192.168.99.101/products'

{"id": "the_odyssey"}
```

#### Get Product

```sh
$ curl 'http://192.168.99.101/products/the_odyssey'

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
$ curl -XPOST -d '{"order_details": [{"product_id": "the_odyssey", "price": "100000.99", "quantity": 1}]}' 'http://192.168.99.101/orders'

{"id": 1}
```

#### Get Order

```sh
$ curl 'http://192.168.99.101/orders/1'

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
