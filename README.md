# Feast Benchmark for Async SDK

The data from this benchmark is generated based on data generator from  https://github.com/feast-dev/feast-benchmarks.

## Setup

### Installation

To install requirements:

```bash
poetry install
```

To activate shell:
```bash
poetry shell
```

Run Redis instance using a Docker container:
```bash
docker-compose up -d
```

### Feast

To apply changes to registry:

```bash
cd registry
```

```bash
feast apply
```

After running this command, the file `registry/registry.db` is updated.

To materialize data to Redis instance:

```bash
feast materialize 2024-05-03 2024-05-04
```

## Running Server

Go back to root folder `cd ..` so you can start the server.

```bash
uvicorn server.server:app --workers 2 --log-level critical
```

Some example commands to request the server:

### Sync endpoint

```bash
curl "http://localhost:8000/get_online_features"
```

Changing the feature service:
```bash
curl "http://localhost:8000/get_online_features?feature_service=feature_service_1"
```

Changing the batch size (number of entity rows):
```bash
curl "http://localhost:8000/get_online_features?feature_service=feature_service_1&batch_size=100"
```

### Async endpoint

```bash
curl "http://localhost:8000/get_online_features_async"
```

Changing the feature service:
```bash
curl "http://localhost:8000/get_online_features_async?feature_service=feature_service_1"
```

## Benchmarking Server

You can use `wrk` or any other load test tool to benchmark the server.
```bash
brew install wrk
```

To start the benchmark execution for sync endpoint:

```bash
wrk --threads 4 --latency "http://localhost:8000/get_online_features?feature_service=feature_service_1"
```

To start the benchmark execution for async endpoint:

```bash
wrk --threads 4 --latency "http://localhost:8000/get_online_features_async?feature_service=feature_service_1"
```
