# Airflow
All these services allow you to run Airflow with [CeleryExecutor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html). For more information, see [Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html).


- [Airflow](#airflow)
  - [Deploy Airflow on Docker](#deploy-airflow-on-docker)
    - [Step 0: Install Docker on Windows workstation](#step-0-install-docker-on-windows-workstation)
    - [Step 1: Fetching docker-compose.yaml](#step-1-fetchingdocker-composeyaml)
    - [Step 2: Initializing Environment](#step-2-initializing-environment)
    - [Step 3: Understanding the yaml file (docker compose file)](#step-3-understanding-the-yaml-file-docker-compose-file)
  - [Initializing Airflow](#initializing-airflow)
    - [Step 1: Initialize the database](#step-1-initialize-the-database)
    - [Step 2: Up the Web Server](#step-2-up-the-web-server)
    - [Step 3: URL](#step-3-url)
    - [Setp 4: remove containers](#setp-4-remove-containers)


## Deploy Airflow on Docker
### Step 0: Install Docker on Windows workstation

This quick-start guide will allow you to quickly get Airflow up and running with CeleryExecutor in Docker.

Caution
This procedure can be useful for learning and exploration. However, adapting it for use in real-world situations can be complicated. Making changes to this procedure will require specialized expertise in Docker & Docker Compose, and the Airflow community may not be able to help you.

For that reason, we recommend using Kubernetes with the Official Airflow Community Helm Chart when you are ready to run Airflow in production.

` Install Docker Community Edition (CE) on your workstation. Depending on your OS, you may need to configure Docker to use at least 4.00 GB of memory for the Airflow containers to run properly. Please refer to the Resources section in the Docker for Windows or Docker for Mac documentation for more information.`

`Install Docker Compose v1.29.1 or newer on your workstation.`

The default amount of memory available for Docker on macOS is often not enough to get Airflow up and running. If enough memory is not allocated, it might lead to the webserver continuously restarting. You should allocate at least 4GB memory for the Docker Engine (ideally 8GB).

You can check if you have enough memory by running this command:

`docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'`


### Step 1: Fetching docker-compose.yaml

To deploy Airflow on Docker Compose, you should fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml).

This file contains several service definitions:

- `airflow-scheduler` - The [scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html) monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- `airflow-webserver` - The webserver is available at `http://localhost:8080`.
- `airflow-worker` - The worker that executes the tasks given by the scheduler.
- `airflow-triggerer` - The triggerer runs an event loop for deferrable tasks.
- `airflow-init` - The initialization service.
- `postgres` - The database.
- `redis` - [The redis](https://redis.io/) - broker that forwards messages from scheduler to worker.

- `./dags` - you can put your DAG files here.
- `./logs` - contains logs from task execution and scheduler.
- `./config` - you can add custom log parser or add `airflow_local_settings.py` to configure cluster policy.
- `./plugins` - you can put your [custom plugins](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html) here.

This file uses the latest Airflow image ([apache/airflow](https://hub.docker.com/r/apache/airflow)). 

If you need to install a new Python library or system library, you can [build your image](https://airflow.apache.org/docs/docker-stack/index.html).


### Step 2: Initializing Environment

Before starting Airflow for the first time, you need to prepare your environment, i.e. **create the necessary files, directories and initialize the database.**

1. Create docker-compose.yaml file and feed it with [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml) content.
2. Create dag folder in root.
3. Create log folder in root.
4. Create plugin folder in root.
5. Create config folder in root.
   
```
├───config
├───dags
├───logs
└───plugins
```

### Step 3: Understanding the yaml file (docker compose file)

This inform us about the docker hub image is beeing chosen for the airflow application.

```
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.7.3}
```

- Volumes (we’ve created at above step)

```
volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
```
---
## Initializing Airflow
### Step 1: Initialize the database

On **all operating systems**, you need to run **database migrations and create the first user account**. To do this, run. Now you need to initialize your container. This step allows you to create all you need to run airflow on your container.

1. Go to wsl terminal

2. Go to the directory where your yaml are
    
3. Apply this following command

```
docker compose up airflow-init
```
    

### Step 2: Up the Web Server

Now you can start all services:
```
docker compose up
```

### Step 3: URL

http://localhost:8080/home

### Setp 4: remove containers
This step is important in case you want to retry the application. If you don't do this, the webserver port won't be available.
```
docker compose down
```
---

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html