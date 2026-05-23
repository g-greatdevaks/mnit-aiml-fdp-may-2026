# Local Telemetry Infrastructure Stack

This directory contains the orchestration configuration required to deploy the local observability services using Docker Compose.

---

## 🐳 Telemetry Stack Services

The local collector infrastructure runs the following containerized services:
* **Jaeger Collector and UI** (`http://localhost:16686`): Receives OpenTelemetry request spans via OTLP and provides a visual timeline interface to trace tool calls and nested model runs.
* **Prometheus Time-Series Database** (`http://localhost:9090`): Dynamically scrapes metrics exported by the Python agent application.
* **Grafana Dashboard Service** (`http://localhost:3000`): Connects to the Prometheus database as a primary data source to visualize live charts of agent latency, token costs, and carbon footprint metrics.

---

## 🚀 Execution Instructions

To launch the telemetry containers in detached daemon mode, navigate to this directory and run the following command:

```bash
docker-compose up -d
```

To stop and remove the active telemetry container instances, run:

```bash
docker-compose down
```

---

## 🛡️ Disclaimer

* The content and views presented during this session are the author's own and not of any organizations they are associated with or employed at.
* **The code shown in this repository is for illustration and educational purposes only.**
  * It is not production-grade; error handling, security, and scalability are not fully addressed.
