```
- ST0263, Challenge 2
- Sebastian Pulido Gomez, spulido1@eafit.edu.co
- Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
```

# MoM and gRPC lab

## 1) Description

## 1.1) Accomplished requirements

The implementation for this lab project has the following accomplishments as required by the lab guide:

- The system is composed of three services, namely, a microservice (M1) implemented with gRPC; a microservice (M2) implemented
  with MoM interfacing; and a gateway service that serves as a proxy in front of M1 and M2.
- M1 was implemented with the gRPC/protocol buffers standard.
- M2 was implemented by interfacing RabbitMQ queues.
- The API gateway exposes a REST API in JSON.
- The API gateway communicates with M1 via gRPC.
- The API gateway communicates with M2 via MoM.
- All of the three services load their boot values via a JSON config file.
- Both M1 and M2 provide the same service, namely, they can list the files available in their assets directory. The
  operation `list` will list all of the files whereas the operation `search` will list specific files that match a pattern.
- The three services (gateway, M1, and M2) allow concurrency.

According to this, all of the requirements specified in the lab guide were accomplished.


## 2) Architecture

The following diagram depicts the system's architecture:

![arch info](./arch-v1.png)

There are two modes the system operates in, namely, gRPC mode and MoM mode. In gRPC mode, when an HTTP client makes a request,
it goes directly to the gateway which in turn serializes the request payload into a specific proto-buffer binary format.
This proto-buffer message is then sent to microservice M1--via gRPC--which deserializes the message and processes the request.
M1 sends the response back--viagRCP--and the API gateway receives and deserializes it via its gRPC client module. Finally,
the gateway dispatches the end response to the HTTP client in JSON format.

In MoM mode, when the HTTP client makes a request, it goes again to the gateway, but this time the request is dispatched to
a request queue served by RabbitMQ. Before the message is pushed to the request queue, a unique request_id is attached to it.
The microservice M2 is a consumer of the request queue, thus whenever there is a new element in it, it polls and deserializes
the message and processes the request. Once the processing is done, M2 serializes the response and pushes it to another queue,
namely, the response queue. The response queue is constantly consumed by the request-threads that are forked by the API gateway.
Thus, whenever there is a new message in this queue, it will be communicated to all of the threads that are currently waiting
to respond to the HTTP client. On a new message, each thread will extract the request_id from it, and will compare it against
the request_id that was initially included in the request. If both ids match, that means that the message corresponds to the
response for the initial request and is thus sent to the HTTP client. If the request_id does not match, the message will be
discarded, and the thread will wait until there is a new message available.


## 3) Development environment

## 3.1) Operating system

This lab project was developed and tested in Ubuntu 22.04.

## 3.2) Programming language

All of the services were implemented in Python 3.10.6. The list of libraries that were used can be seen in the requirements.txt
file of this project:

```
Flask==2.2.3
grpcio-tools==1.51.3
grpcio==1.51.3
pika==1.3.1
```

Flask was used to implement the API gateway, pika is the RabbitMQ client library used to implement M1, and grpcio* is
the gRPC toolkit library used to implement M1.


## 3.3) Docker

Docker and docker-compose were used to set up a container with a RabbitMQ service. The version of docker-compose is
v2.3.3 and the version of Docker is 23.0.1.

## 3.4) Dir tree

![dir-tree](dir-tree.jpeg)

## 3.5) Build process

All of the installation and build processes for this lab were automated via `bash scripting` and `make`. At the root of this project,
there is an [installation script](first-time-install.sh) for all of the system dependencies required to run the project. Please
run the following:

```
./first-time-install.sh
```

Once all of the dependencies are installed, restart your shell session so that you can run docker without sudo.

The Python dependencies are handled via virtual environments. Please, run the following make rule in order to setup the
Python virtual environment:

```
make set-py-venv-with-deps
```

Note that all of the build scripts for the Python services are handled via a [Makefile](Makefile).


## 3.6) RabbitMQ setup

To run the RabbitMQ service run:

```
cd docker
./service.sh up
```

This will start up a RabbitMQ instance at port 5672 on the host machine. The admin console can be reached at port 8088
on the host machine. You can modify these ports by tweaking the settings in `docker/docker-compose.yaml`.

To create the queues and exchanges necessary to run the project, please run the following make rule at the root of the
project:

```
make rabbit-setup
```

This rule just executes a python script defined in `mom-setup/__main__.py`. You can tweak the credentials, host and port
in this script depending on the settings in your docker-compose.yaml file.


## 3.7) Microservice configuration

The microservices are located in the following directories: `micro1-grpc`, `micro2-mom`, and `gateway`. Inside each of
these directories there is a `config.json` file that you can edit depending on your system parameters.

For `micro1-grpc` we have the following settings:


```
{
  "port": 50051,
  "max_workers": 10,
  "dir_path": "absolute/path/to/assets/dir"
}
```

Where `port` is the port the gRPC server is going to listen on, `max_workers` is the maximum number of worker threads that
will serve the application, and `dir_path` is the assets directory whose files will be listed by the service.

For `micro2-mom` we have the following settings:


```
{
  "dir_path": "absolute/path/to/assets/dir"
  "rabbit_user": "admin",
  "rabbit_password": "secret",
  "rabbit_host": "127.0.0.1",
  "rabbit_port": "5672"
}
```

where `dir_path` is the same as for `micro2-grpc`, `rabbit_user` and `rabbit_password` are the RabbitMQ credentials, and
`rabbit_host` and `rabbit_port` are the host and port where RabbitMQ is running, respectively.

For `gateway` we have the following settings:


```
{
  "host": "127.0.0.1",
  "port": 8001,
  "grpc_host": "127.0.0.1",
  "grpc_port": 50051,
  "rabbit_user": "admin",
  "rabbit_password": "secret",
  "rabbit_host": "127.0.0.1",
  "rabbit_port": 5672
}
```

where `rabbit-*` is the same as for `micro2-mom`, `grpc_host` and `grpc_port` are the host and port where `micro1-grpc`
is running. Finally, `host` and `port` specify the IP and port where the `gateway` is going to be served.


## 3.7) Microservice execution

There are make rules to execute the services:

```
make run-m1
make run-m2
make run-gateway
```

You can execute the above rules in different terminals, and logs will be displayed.

## 3.8) Implementation details

### 3.8.1) Protocol buffers

The gRPC protocol for this project can be found in `protos/file_service.proto`

```
...

service FileService {
  rpc ListFiles (ListFilesRequest) returns (FilesReply) {}
  rpc SearchFiles (SearchFilesRequest) returns (FilesReply) {}
}

message ListFilesRequest {
  optional int32 limit = 1;
}

message SearchFilesRequest {
  string pattern = 1;
  optional int32 limit = 2;
}

message FilesReply {
  string file_list = 1;
}

```

Basically, we have two operations `ListFiles` and `SearchFiles`, which return both a list of files. A simple ListFiles
operation can only specify the limit of files to be listed. On the other hand, a SearchFiles operation can additionally
specify a pattern to match specific files.

There is a make target to build the proto-buff modules:

```
make build-proto
```

This rule produces the following python modules: `micro1-grpc/src/file_service_pb2_grpc.py`, `micro1-grpc/src/file_service_pb2.py`
and `micro1/src/file_service_pb2.pyi`. These modules contain all of the utilities to serialize/deserialize and send/receive
messages via out custom protocol.

### 3.8.2) micro1-grpc and micro2-mom

micro1-grpc is a gRPC server that communicates via protocol-buffers standard. It provides the services explained in the
previous section and its main routine can be found in `micro1-grpc/src/__main__.py`. Notice that it is mostly using the
modules that were generated automatically by the `grpcio-tools` library to handle the serialization/deserialization and
communication through our custom protocol buffers.

micro2-mom performs the very same operations as micro1-grpc but it is basically a consumer of the request queue and a producer
to the response queue served by RabbitMQ service. Thus, its communication path follows the MoM path described in section 2. Its
main routine can be found in `micro2-mom/src/__main__.py`.


### 3.8.3) gateway

The API gateway is basically a Flask HTTP server that receives requests from HTTP clients and dispatches them to either
micro1-grpc or micro2-mom. In order to do this, the gateway has to implement client modules that interface with these two
micro-services via gRPC and MoM, respectively. The gateway's gRPC client implementation can be found in `gateway/src/files_grpc.py`,
and the MoM client implementation can be found in `gateway/src/files_mom.py`.

Notice that at the API definition level (`gateway/src/__api__.py`), there is the following mutex:

```
mode_mutex = Lock()
```

this mutex is used to switch between gRPC and MoM modes, namely, whenever a request is received, the request thread must
acquire the lock in order to toggle the following application variable:

```
app.config["IS_GRPC"]
```

If this variable is `True` the request will be served in gRPC mode. However, if False, it'll be served in MoM mode.
Thus, the API gateway will switch between MoM and gRPC across multiple requests.

## 4) Deployment on AWS cloud

This project lab is deployed in an EC2 instance (`spulido1-mom-grpc`) on the AWS academy cloud. The type of machine chosen
for this project is a `t2.micro` with an Ubuntu-22.04 image:

![ec2-instance](./ec2-instance.jpeg)

The instance has the following security groups which allow inbound access to port 22 via SSH, and ports 80 and 8080 via TCP:

![sec-groups](./sec-groups.jpeg)


There was nothing special about the deployment setup in this environment. In a SSH session with the aws instance the project
repo was cloned at `/opt`:


```
cd /opt
git clone https://github.com/sebashack/spulido1-st0263.git
```

The API gateway was configured to be served on port 80 and the build and execution scripts were run as explained above.

Finally, the following service files were created for each microservice:

```
[Unit]
Description=File service grpc

[Service]
User=root
WorkingDirectory=/opt/spulido1-st0263/challenge2
ExecStart=make run-m1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```
[Unit]
Description=File service mom

[Service]
User=root
WorkingDirectory=/opt/spulido1-st0263/challenge2
ExecStart=bash -c "make rabbit-setup && make run-m2"
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```
[Unit]
Description=File service gateway

[Service]
User=root
WorkingDirectory=/opt/spulido1-st0263/challenge2
ExecStart=bash -c "make rabbit-setup && make run-gateway"
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

And the following commands were run to load the services in systemd:

```
sudo systemctl daemon-reload
sudo systemctl enable filemom.service
sudo systemctl enable filegrpc.service
sudo systemctl enable gateway.service

sudo systemctl start filemom.service
sudo systemctl start filegrpc.service
sudo systemctl start gateway.service
```

This means that our project will be automatically started when the EC2 instance boots. To check that it works, just send
a request to the IP address that is dynamically attached to the `spulido1-mom-grpc` instance. For example, if the IP turns
out to be `100.26.152.121` (remember that the gateway is served on port 80):

```
curl '100.26.152.121/files/list?limit=2'
```


## 5) User guide

The API gateway exposes 2 endpoints:

- `/files/list`: Lists all of the files served by this service. It accepts and optional parameters curl `/files/list?limit=<int>`
                 where `limit` is the maximum number of files to be retrieved.
- `/files/search`: Lists all files that match a given pattern. These patterns work the same way as with the GNU linux `find` command.
                   For example, `/files/search?pattern=*.png` will only list the files that have `png` extension. This endpoint also
                   accepts the `limit` parameter.

You can use a client such as Curl to test these endpoints. The following example interactions show the server replies for
an EC2 instance with IP `54.157.179.1`:

```
curl '54.157.179.1/files/list?limit=2'

Response:

{"files":["/home/ubuntu/spulido1-st0263/challenge2/assets/snap.jpg","/home/ubuntu/spulido1-st0263/challenge2/assets/sample-txt.txt"],"found":13,"provider":"grpc","status":200}
```

```
curl '54.157.179.1/files/search?limit=4&pattern=*.txt'

Response:

{"files":["/home/ubuntu/spulido1-st0263/challenge2/assets/sample-txt.txt","/home/ubuntu/spulido1-st0263/challenge2/assets/text1.txt","/home/ubuntu/spulido1-st0263/challenge2/assets/questions.txt","/home/ubuntu/spulido1-st0263/challenge2/assets/poetry.txt"],"found":4,"provider":"mom","req_id":"4df97d96-7765-46fe-b57a-e946bd065ebc","status":200}
```

Notice that the `provider` field indicates whether the request was resolved via gRPC or MoM.


## 6) References

- https://grpc.io/docs/languages/python/basics
- https://github.com/grpc/grpc/tree/v1.52.0/examples/python/helloworld
- https://www.rabbitmq.com/tutorials/tutorial-six-python.html
- https://flask.palletsprojects.com/en/2.2.x/quickstart
