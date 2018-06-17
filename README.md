# flask-rest-server

Small REST API created in Python with Flask and SQLAlchemy. Application uses SQLite as database engine and implements all CRUD operations using HTTP methods.

## Table of Contents
* [Models](#models)
* [Endpoints](#endpoints)
* [Requests](#requests)
  * [Examples](#examples)
* [Running](#running)
* [Tests](#tests)

## Models
There are two models - **Client** and **Dataset** - containing following fields:
1. Client
 a) name - full name of client
 b) IP address of client (IPv4 or IPv6 are allowed)
2. Dataset
 a) client - ID of client being dataset's owner
 b) filename - name of data file (max. 255 characters)
 c) any other key-value pair (user-defined metadata)

Each client can have multiple datasets, but single dataset can be connected only to one client.

## Endpoints

* /clients
  * GET - return list of all clients
  * POST - create new client
* /clients/<client_id>
  * GET - return details of specific client
  * PATCH - (partially) update client
  * DELETE - delete client
* /datasets
  * GET - return list of all datasets
  * POST - create new dataset
* /datasets/<dataset_id>
  * GET - return details of specific dataset
  * PATCH - (partially) update dataset
  * DELETE - delete dataset

## Requests

Requests should be send with JSON in message's body. Full specification of all requests there is accessible in auto-generated Swager UI which is available at /api/spec.html (by default: http://127.0.0.1:5000/api/spec.html#!/spec) after starting REST server. It also allows for interacting with API without having to use the console tools. Just click "Try it out!" button to send your request directly to the server. 

![](https://raw.githubusercontent.com/trivelt/img-resources/master/flask-swagger.png)

#### Examples

```curl --request POST --header "Content-Type: application/json" --data '{"name": "Foo","ip_address": "127.0.0.1"}' http://127.0.0.1:5000/clients -v```
```javascript
POST /clients
{
  'name': 'Foo',
  'ip_address': '127.0.0.1'
}
```
 \
```curl --request PATCH --header "Content-Type: application/json" --data '{"client": 5, "executable": "True"}' http://127.0.0.1:5000/datasets/2 -v```
```javascript
PATCH /datasets/2
{
  'client': 5,
  'executable': 'True'
}
````

## Running
To launch flask-rest-server following dependencies must be met:
* System packages: python3, python3-pip
* Python packages: flask, flask-api, flask-restful, flask-restful-swagger, flask-sqlalchemy, IPy, sqlalchemy

Instead of downloading required packages locally you can use prepared Docker image contaning whole application and all dependencies.

```sh
docker pull trivelt/flask-rest-server:latest
docker run --rm --net=host trivelt/flask-rest-server:latest bash -c ./start_rest.py
```

You can also build Docker image yourself using Dockerfile from this repository:
```sh
cd flask-rest-server
docker build -t flask-rest-server:latest .
```
If you want you can run interactive docker session and use your own config specifying optional parameter --config:

```sh
$ sudo docker run -it --net=host trivelt/flask-rest-server:latest
REST-DOCKER:~$ ./start_rest.py --config debug.cfg 
```
## Tests

There is `tests` directory which contains set of component tests (about 40 test cases). In order to run them type:
````sh
cd rest_server/ && ./run_tests.sh
````
or using pulled Docker image:
````sh
docker run --rm trivelt/flask-rest-server:latest /bin/bash -c ./run_tests.sh
````

