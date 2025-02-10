# PictuRAS Watermark Tool MS

This project implements the watermark tool microservice for **PictuRAS**.

[![Docker Hub](https://img.shields.io/docker/pulls/prcsousa/picturas-watermark-tool-ms)](https://hub.docker.com/r/prcsousa/picturas-watermark-tool-ms)

Processes image watermarking requests asynchronously using a message queue.

It is based on three main services:

1. RabbitMQ message-broker: handles queuing of processing requests and returning results.
2. request mocker: publishes mock requests to the queue.
3. the watermark tool microservice: processes the requests and publishes results.

> This project includes a `request mocker` under `usage_example` folder to ease development. The requests should eventually be produced by a _real microservice_ (e.g., a project management service).

In detail, after a request is sent, one of the watermark tool microservices reads it from their queue, applies the watermark, and saves the watermarked image. After having processed a given request, a `ResultMessage` is sent to `picturas.tools` _exchange_ under the `results` _routing key_.

## Project structure

1. **Watermark microservice (`picturas_watermark_tool_ms/`):**

   This folder contains the service logic for processing watermark requests and applying watermarks to images. It includes key modules such as:

   - `main.py`: The entry point of the microservice, instantiating tool specific classes and starting message processing.
   - `config.py`: Defines service-specific configurations, including the watermark image and message queue endpoints.
   - `watermark_tool.py`: Implements the logic for watermarking images, extending the reusable core components.
   - `watermark_request_message.py` & `watermark_result_message.py`: Define format and data of watermark request and result messages.

2. **Core components (`picturas_watermark_tool_ms/core/`):**

   This folder contains generic, reusable modules designed to support multiple tools within the `PictuRAS` system, if wanted. These components abstract common functionalities, allowing them to be easily integrated into other tool microservices.

3. **Usage Example (`usage_example/`):**

   A demonstration environment that showcases how to use the watermarking microservice.

This design emphasizes modularity, with reusable components in the `core/` folder that can accelerate development and standardize functionality across multiple tool microservices in the `PictuRAS` ecosystem.

> One may create new tool microservices by cloning this project and implementing the specific `Tool`, `RequestMessage` (Parameters) and `ResultMessage` classes.

# How to run

## Requirements

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- [RabbitMQ](https://www.rabbitmq.com/tutorials)
- [Docker](https://docs.docker.com/engine/install/)

## Running _Usage example_

Follow the steps below to run the usage example for the watermarking microservice:

1. Navigate to `usage_example` directory:

   ```bash
   cd usage_example
   ```

2. Start the services using Docker Compose:
   ```bash
   docker compose up
   ```

This will start the watermark tool microservice along with the message-broker and the request mocker.
The request mocker will send sample watermarking requests using the images provided in the `./images/src/` folder, and the processed images will be saved in the `./images/out/` folder.

For further customization or testing, you can modify the request mocker script, or replace the sample images in the `./images/src/` folder.

## Development

### 1. Run RabbitMQ (message-broker)

This tool relies on RabbitMQ to subscribe and publish messages, so we need it running.
One way of doing it is using Docker:

```bash
docker run -p 5672:5672 -p 15672:15672 rabbitmq:4-management-alpine
```

> Ports `5672` and `15672` are exposed to host so you can:
>
> 1. connect your local publishers and subscribers using `localhost` and port `5672`
> 2. access RabbitMQ dashboard from your browser at http://localhost:15672 (default credentials: `guest` / `guest`)

### 2. Install dependencies

```bash
poetry install
```

### 3. Run both _Request mocker_ and _Watermark tool_

1. Start request mocker

```bash
source $(poetry env info --path)/bin/activate
python -m usage_example.request_mocker.main
```

2. Run watermark tool in another bash

```bash
source $(poetry env info --path)/bin/activate
python -m picturas_watermark_tool_ms.main
```

> Tip: if you use VSCode you'll find some handy configurations on "Run and Debug" section

## Environment variables

The application uses several environment variables for configuration. Below is a summary table detailing each variable, its purpose, and default value.

| **Environment Variable**        | **Description**                                | **Default Value**            |
| ------------------------------- | ---------------------------------------------- | ---------------------------- |
| `RABBITMQ_HOST`                 | The hostname of the RabbitMQ server.           | `localhost`                  |
| `RABBITMQ_PORT`                 | The port number for the RabbitMQ server.       | `5672`                       |
| `RABBITMQ_USER`                 | The username for authenticating with RabbitMQ. | `guest`                      |
| `RABBITMQ_PASS`                 | The password for authenticating with RabbitMQ. | `guest`                      |
| `RABBITMQ_REQUESTS_QUEUE_NAME`  | The RabbitMQ queue name for requests.          | `watermark-requests`         |
| `RABBITMQ_RESULTS_EXCHANGE`     | The RabbitMQ exchange name to publish results. | `picturas.tools`             |
| `RABBITMQ_RESULTS_ROUTING_KEY`  | The RabbitMQ routing key to publish results.   | `results`                    |
| `PICTURAS_LOG_LEVEL`            | The logging level for the application.         | `INFO`                       |
| `PICTURAS_MS_NAME`              | The name of the microservice instance.         | `picturas-watermark-tool-ms` |
| `PICTURAS_NUM_THREADS`          | The number of threads used by the application. | `4`                          |
| `PICTURAS_WATERMARK_IMAGE_PATH` | The file path to the watermark image.          | `./watermark.png`            |

### Notes

- **Custom Configuration**: All variables can be overridden by setting them in the environment.
- **Defaults**: If a variable is not set, the default value will be used as indicated in the table.
- **Critical Variables**: Ensure `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, and `RABBITMQ_PASS` are correctly configured for RabbitMQ connectivity.
