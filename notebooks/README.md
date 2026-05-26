# Agent Observability Laboratory Notebooks

This directory contains the master agenda slide notebook and four sequential hands-on lab exercises for the Faculty Development Programme on **Observability for AI Agents**.

---

## 🗺️ Notebook Roadmap

1. **[00_curriculum_and_agenda.ipynb](00_curriculum_and_agenda.ipynb)**: The master presentation slide notebook. It contains the FDP schedule, slide summaries for each topic, and hyperlinked roadmap indexes.
2. **[01_structured_logging_cost_carbon.ipynb](01_structured_logging_cost_carbon.ipynb)**: Lab 1. Covers structured logging configurations using `structlog` to emit JSON-formatted telemetry, cost tracking (FinOps), and carbon footprint calculation (GreenOps) via `codecarbon`.
3. **[02_distributed_tracing_react_agent.ipynb](02_distributed_tracing_react_agent.ipynb)**: Lab 2. Covers distributed request tracing using the OpenTelemetry SDK to record parent-child span correlations inside a ReAct agent loop, exporting spans to Arize Phoenix or Jaeger.
4. **[03_metrics_evaluation_alerting_profiling.ipynb](03_metrics_evaluation_alerting_profiling.ipynb)**: Lab 3. Covers telemetry metric aggregation, Python code profiling via the native `cProfile` and `pstats` modules to isolate execution bottlenecks, automated evaluations, and alerting rules.
5. **[04_sandbox_isolation_safety_guardrails.ipynb](04_sandbox_isolation_safety_guardrails.ipynb)**: Lab 4. Covers secure code execution inside process-isolated sandboxes with OS resource limit controls, stack-based WebAssembly (WASM) virtual machine simulations, input/output safety guardrails (including direct jailbreak scanners and Data Loss Prevention/PII redactions), and egress gateway proxy allowlists in alignment with [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) specifications.

---

## 🚀 Usage Instructions

The Jupyter Notebook server is initiated from the command line:

```bash
jupyter notebook
```

Within the browser interface, navigate to this folder and open `00_curriculum_and_agenda.ipynb` to begin.

---

## 🛡️ Disclaimer

* The content and views presented during this session are the author's own and not of any organizations they are associated with or employed at.
* **The code shown in this repository is for illustration and educational purposes only.**
  * It is not production-grade; error handling, security, and scalability are not fully addressed.
