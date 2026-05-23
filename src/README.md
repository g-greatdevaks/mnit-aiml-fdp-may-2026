# Application Source Modules

This directory contains the Python module implementations utilized across the laboratory notebooks to simulate Large Language Model (LLM) calls and integrate local inference endpoints.

---

## 📁 Modules

* **[mock_llm.py](mock_llm.py)**: Contains class definitions for simulating model inference transactions:
  * `MockLLMResponse`: A container class capturing generated text output, token consumption metrics (input and output), and estimated financial costs.
  * `MockLLMClient`: A stateless simulation client that mocks natural network inference latency and returns deterministic responses matching ReAct reasoning loop prompts.
  * `OllamaLLMClient`: An HTTP wrapper client that connects to local Ollama API daemons (e.g., executing open-source models like Llama3 or Qwen) to return actual model completions, token statistics, and latencies.

---

## 🛡️ Disclaimer

* The content and views presented during this session are the author's own and not of any organizations they are associated with or employed at.
* **The code shown in this repository is for illustration and educational purposes only.**
  * It is not production-grade; error handling, security, and scalability are not fully addressed.
