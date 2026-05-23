# Faculty Development Programme: Observability, FinOps, and GreenOps for AI Agents (May 2026)

This repository contains hands-on lab materials for the **Observability for AI Agents** session. The curriculum focuses entirely on **open-source, local-first, zero-signup Python tools** to avoid any dependencies on credit cards, external cloud resources, or payment setups.

While the curriculum, code modules, and laboratory exercises are implemented using Python, similar observability architectures, logging processors, OpenTelemetry SDK boundaries, and profiling paradigms are supported across other language ecosystems (including Node.js, Go, Java, and Rust).

---

## 🤖 Traditional Monitoring vs. LLM vs. Agent Observability

| Dimension | Traditional APM | LLM Monitoring | Agent Observability |
| :--- | :--- | :--- | :--- |
| **System Model** | Deterministic (where identical inputs yield predictable, identical outputs), request-response | Non-deterministic (where outputs can vary on identical inputs), single-turn model calls (where a single prompt receives a single completion without memory of past messages) | Multi-turn reasoning loops (where the agent iterates through multiple thoughts and actions), tool calls (invoking external functions or databases) |
| **Core Metrics** | CPU, Memory, Disk, and HTTP Error Rate | Input and output tokens, prompt cost, and end-to-end latency | Tool execution latency, steps-per-run, and cost |
| **Telemetry Needs** | Logs, Metrics, and distributed tracing (tracking a request path across multiple modules) | Linear trace context (tracking simple start-to-end execution), and cost calculation | Nested parent-child traces (hierarchical trace trees), and execution graphs |

---

## 🍃 Redefining the Five Pillars of Agent Observability

1. **Traces**: Tying complex agent reasoning loops (thoughts, tool runs, and nested sub-agent calls) to a single root trace context (the overall transaction path) using **OpenTelemetry**.
2. **Structured Logs**: Emitting JSON-formatted logs with embedded contextual IDs (Session ID, User ID, Version, and Trace ID) using **structlog**.
3. **FinOps (Cost Tracking)**: Tracking token costs of input and output requests per model to prevent runaway costs from agent loops.
4. **GreenOps (Environmental footprint)**: Measuring CPU/GPU energy consumption (kWh) and carbon emissions ($CO_2e$) of local/remote inference using **CodeCarbon**.
5. **Profiling and Guardrails**: Surgical profiling of slow tool methods (using `cProfile`) and applying runtime guardrails (e.g. input and output validation, and prompt injection protection).

---

## 📁 Repository Structure

```text
mnit-aiml-fdp-may-2026/
├── README.md                          # This file (curriculum guide and setup)
├── requirements.txt                   # Local Python package dependencies (structlog, codecarbon, etc.)
├── docker/
│   ├── docker-compose.yml             # Jaeger, Prometheus, and Grafana stack
│   └── prometheus.yml                 # Prometheus scrape job configuration
├── notebooks/
│   ├── 00_curriculum_and_agenda.ipynb # Master Syllabus and Slide Agenda
│   ├── 01_structured_logging_cost_carbon.ipynb     # Lab 1: Structured Logging, FinOps, and GreenOps
│   ├── 02_distributed_tracing_react_agent.ipynb    # Lab 2: Distributed Tracing and Tool Calls
│   └── 03_metrics_evaluation_alerting_profiling.ipynb # Lab 3: Metrics, Evaluations, Alerting, and Profiling
└── src/
    ├── __init__.py
    └── mock_llm.py                    # Mock LLM and Ollama API wrappers for agent calls
```

---

## 🚀 Getting Started

### 1. Installation and Python Setup
The terminal is opened, the working directory is navigated to this path, and the virtual environment is configured:

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt
```

### 2. Launching Jupyter Notebooks
The Jupyter Notebook server is initiated via the following command:
```bash
jupyter notebook
```
The user navigates to the `notebooks/` directory and opens `00_curriculum_and_agenda.ipynb` to begin.

---

## 🐳 Running the Local Telemetry Stack (Grafana, Prometheus, and Jaeger)

For a complete local visual dashboard experience, a telemetry collector stack is executed locally:

```bash
# Navigate to the docker directory and start containers
cd docker
docker-compose up -d
```

#### Services Started:
* **Jaeger Dashboard**: **`http://localhost:16686`** (to visualize OpenTelemetry spans and agent tool execution trees).
* **Prometheus UI**: **`http://localhost:9090`** (to query live scraper metrics).
* **Grafana Dashboards**: **`http://localhost:3000`** (default login: `admin` / `admin`). Prometheus is configured as the primary data source to visualize live charts for agent latency, token costs, and carbon footprint metrics.

---

## 🦙 Running with Local Models (Ollama)

To replace the offline **Mock LLM Client** with a local, active large language model:

1. [Ollama](https://ollama.com/) is downloaded and installed.
2. A lightweight model is pulled (e.g., Qwen 0.5B or Llama3):
   ```bash
   ollama pull qwen2.5:0.5b
   ```
3. Within the notebooks, the client initialization is updated:
   ```diff
   -from src.mock_llm import MockLLMClient
   -llm_client = MockLLMClient()
   +from src.mock_llm import OllamaLLMClient
   +llm_client = OllamaLLMClient(model_name="qwen2.5:0.5b")
   ```
4. Upon executing the cells, tracing spans and structured logs automatically capture the model outputs, costs, emissions, and latencies.

---

## 📦 Containerized Execution (Alternative Setup)

To execute the lab environment inside an isolated Docker container instead of configuring a local host Python virtual environment, the provided `Dockerfile` and `.dockerignore` files can be leveraged.

### 1. Building the Docker Image
To build the containerized workspace image, run the following command from the root of this directory:

```bash
docker build -t agent-observability-workspace .
```

### 2. Running the Container
To run the containerized Jupyter Notebook server, map the notebook interface port (8888) and telemetry span exporter port (6006) to the host system:

```bash
docker run -it -p 8888:8888 -p 6006:6006 agent-observability-workspace
```

Upon execution, the Jupyter Notebook server logs will output a tokenized URL (e.g., `http://127.0.0.1:8888/?token=...`). The URL is copied and pasted into a web browser to access the curriculum notebooks.

---

## 🔍 Diagnostic Setup Verification

To verify that all required Python packages (e.g., `structlog`, `codecarbon`, and OpenTelemetry SDKs) are successfully configured and can resolve dependencies, the `verify_setup.py` diagnostics tool is provided at the workspace root. 

The diagnostic check is executed using the virtual environment interpreter:

```bash
python verify_setup.py
```

---

## 📚 Detailed Syllabus

### Module 1: Introduction to AI Agent Observability
* **Lecture**: Traditional APM, LLM, and Agent monitoring.
* **Concepts**: Sense-Think-Act loops, agent non-determinism, and the shift from Logs, Metrics, and Traces to the 5 Pillars of Observability (FinOps, GreenOps, Profiling, Traces, and Logs).

### Module 2: Structured Logging, FinOps, and GreenOps ([01_structured_logging_cost_carbon.ipynb](notebooks/01_structured_logging_cost_carbon.ipynb))
* **Hands-on**: Instrumenting `structlog` for machine-readable JSON logs.
* **GreenOps Integration**: Setting up `codecarbon` (Offline Mode) to measure energy consumption and $CO_2$ emissions.
* **FinOps Integration**: Tracking token usage and costs per inference.
* **Production Guidelines**: Implementing asynchronous log writing (Vector or FluentBit), PII and credential redaction (via [Google Cloud Sensitive Data Protection](https://cloud.google.com/sensitive-data-protection), [Microsoft Presidio](https://github.com/microsoft/presidio), [Scrubadub](https://github.com/scrubadub/scrubadub), or regex filters), log volume management (dynamic log levels), sparse event schemas to prevent empty key indexing bloat, semantic caching (e.g., using [GPTCache](https://github.com/zilliztech/GPTCache)) with cost and carbon savings telemetry, and carbon-aware batch scheduling (relying on [Electricity Maps](https://www.electricitymaps.com/) or [WattTime](https://www.watttime.org/) marginal carbon intensity metrics to avoid peak peaker plant emissions) in green datacenters.

### Module 3: Distributed Tracing and Alternative Backends ([02_distributed_tracing_react_agent.ipynb](notebooks/02_distributed_tracing_react_agent.ipynb))
* **Theory**: Understanding the evolution of open telemetry standards (OpenTracing trace API specifications, OpenCensus metrics and traces SDK implementations, and their consolidation into standard OpenTelemetry).
* **Hands-on**: Building a ReAct reasoning agent loop.
* **OTel Integration**: Creating OTel spans for LLM calls and tool executions.
* **Visualization**: Spawning Arize Phoenix locally (via Python CLI `phoenix serve` or running the `arizeai/phoenix` Docker container) and learning to export standard OTel traces to Jaeger/Langfuse.
* **Production Guidelines**: Deploying local OpenTelemetry Collector sidecars to offload transport latency, configuring tail-based trace sampling, and setting maximum span attribute limits to prevent payload bloat.

### Module 4: Agent Metrics, Evaluations, Alerting, and Profiling ([03_metrics_evaluation_alerting_profiling.ipynb](notebooks/03_metrics_evaluation_alerting_profiling.ipynb))
* **Theory**: Understanding OpenTelemetry Metric Readers (pull-based Prometheus Metric Readers vs. push-based OTLP Metric Exporters).
* **Metrics**: Client-side UX metrics (TTFT and inter-token latency) vs. Server-side system metrics (step counts, tool bottlenecks, and KV cache utilization and hit ratios).
* **Profiling**: Hands-on Python profiling with `cProfile` and `pstats` to isolate slow tools, thread dump diagnostics (`faulthandler` and `jstack`) to isolate hanging runtime socket reads, and heap memory audits (`tracemalloc`) to detect memory leaks.
* **Alerts and Evals**: Setting alerting thresholds on latency and costs, and writing deterministic correctness evaluations.
* **Production Guidelines**: Exposing asynchronous Prometheus scrape endpoints, routing alerting notifications via Alertmanager or PagerDuty with PromQL policies, and running continuous low-overhead profiling agents (Pyroscope).

### Module 5: Deployment Topologies, Governance, Security, Health, and Data Observability
* **Deployment Topologies**:
  * **VMs**: Local logging, journald, and log forwarding agents (Vector or FluentBit).
  * **Kubernetes (K8s)**: DaemonSet collectors, pod endpoint scrapers, and scalable deployments.
  * **SaaS/PaaS**: Ephemeral execution (e.g., AWS Fargate and GCP Cloud Run) and external SaaS telemetry endpoints (LangSmith and Langfuse Cloud).
* **eBPF (Kernel-Level Observability)**: Zero-instrumentation monitoring of network calls, HTTP and gRPC requests to LLM providers, TLS handshakes, and database queries. Native integrations include the official OpenTelemetry Go Auto-Instrumentation agent and Grafana Beyla.
* **Governance Tracking**: Safety guardrails and Data Loss Prevention (DLP) compliance logging (PII detection via [Google Cloud Sensitive Data Protection](https://cloud.google.com/sensitive-data-protection), [Microsoft Presidio](https://github.com/microsoft/presidio), or [Scrubadub](https://github.com/scrubadub/scrubadub), toxicity classification), execution provenance audit logs, and tracking model drift and bias.
* **Security and Threat Observability**: Real-time tracking of indirect prompt injections, data exfiltration attempts, excessive tool agency, inline guardrail logs (Llama Guard and NeMo Guardrails), hashed API key alias monitoring, role-based access control (RBAC) tool validation checks, and API quota rate-limit header metrics.
* **Vulnerability and Sandbox Telemetry**: Auditing untrusted, model-generated code execution inside secure sandboxes (e.g., microVMs, WebAssembly, or local chroot jails). Remediations include CPU and memory limits, system call (syscall) interception, read-only root filesystems, and strict serverless execution timeouts.
* **Shadow APIs and Latent Threats**: Monitoring dynamic outbound connections (to detect unregistered "Shadow APIs" spawned by agent tools) and tracking latent vulnerabilities. Remediations include Secure Egress Forward Proxies with domain allowlisting, network routing isolation (local OS firewalls, cloud VPC security groups, or Kubernetes NetworkPolicies), and inline safety guardrail scanners (Llama Guard).
* **Operational Health Probes**: Setting up liveness and readiness endpoint checks, monitoring downstream API reachability (Ollama and OpenAI), database availability, and chat history memory leakage.
* **Data Observability and RAG Lineage**: Tracking data lineage from source documents (`manual.pdf` -> chunks), monitoring retrieval context freshness and staleness, context relevance, and groundedness metrics.

---

## 🎙️ Speaker

### Anmol Krishan Sachdeva
* **Title**: Sr. Solutions Engineer (Platform Engineering), Google
* **LinkedIn**: [@greatdevaks](https://www.linkedin.com/in/greatdevaks)
* **Twitter**: [@greatdevaks](https://www.twitter.com/greatdevaks)
* **Sessionize**: [sessionize.com/greatdevaks](http://sessionize.com/greatdevaks)

---

## 🛡️ Disclaimer

* The content and views presented during this session are the author's own and not of any organizations they are associated with or employed at.
* **The code shown in this repository is for illustration and educational purposes only.**
  * It is not production-grade; error handling, security, and scalability are not fully addressed.
