"""
Module: mock_llm
Description: Provides mock and local LLM clients to simulate model inferences.
             It includes standard structured response formats, simulation latency,
             and local network integration with Ollama services.
"""

import time
import random
from typing import Dict, Any

class MockLLMResponse:
    """
    Represents the structured response returned by LLM clients.

    Attributes:
        text (str): The generated completion content.
        prompt_tokens (int): The estimated or actual token count of the input prompt.
        completion_tokens (int): The estimated or actual token count of the generated response.
        cost (float): Calculated USD cost of the inference request.
    """
    text: str
    prompt_tokens: int
    completion_tokens: int
    cost: float

    def __init__(self, text: str, prompt_tokens: int, completion_tokens: int) -> None:
        """
        Initializes the MockLLMResponse with standard token estimation and USD cost calculation.
        
        Args:
            text (str): Raw text of the completion.
            prompt_tokens (int): Count of input tokens.
            completion_tokens (int): Count of output tokens.
        """
        self.text = text
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        
        # Production cost tracking: Cost is based on estimated rates of $15/1M input and $60/1M output tokens.
        self.cost = (prompt_tokens * 15.0 / 1e6) + (completion_tokens * 60.0 / 1e6)


class MockLLMClient:
    """
    Simulates a remote Large Language Model API client.
    Designed for zero-dependency local lab testing.
    """
    base_delay: float
    jitter: float

    def __init__(self, base_delay: float = 0.4, jitter: float = 0.2) -> None:
        """
        Initializes the MockLLMClient with configurable latency and jitter.

        Args:
            base_delay (float): The baseline time delay in seconds.
            jitter (float): The maximum variance in delay to simulate natural network congestion.
        """
        self.base_delay = base_delay
        self.jitter = jitter

    def generate(self, prompt: str) -> MockLLMResponse:
        """
        Simulates model text generation with network delay and token count estimation.
        Recognizes specific prompt patterns to enable agent loop state transitions.

        Args:
            prompt (str): The input query or system prompt.

        Returns:
            MockLLMResponse: Structured token, content, and cost response.
        """
        # Latency Simulation: Emulates standard network request processing times
        # Adds a random delay variation to the base latency to simulate real network fluctuation
        delay: float = self.base_delay + random.uniform(-self.jitter, self.jitter)
        # Blocks the executing thread for the calculated duration (minimum 0.1 seconds)
        time.sleep(max(0.1, delay))

        # Token count estimation: Assumes an average word/token compression of 4 characters per token
        prompt_tokens: int = max(1, len(prompt) // 4)
        # Normalizes the prompt input text (stripping surrounding whitespaces and converting to lowercase)
        prompt_clean: str = prompt.strip().lower()

        # Deterministic ReAct loop matching rules:
        # Step 1 of ReAct: If the user query is detected and search results are not yet present in context history
        if "population of france multiplied by 2" in prompt_clean and "68 million" not in prompt_clean:
            # Emulates the model deciding to search the web for the population data
            response_text = (
                "Thought: I need to find the population of France first.\n"
                "Action: search(\"population of France\")"
            )
        # Step 2 of ReAct: If the search output (68 million) has been appended to context, but math hasn't been calculated
        elif "population of france" in prompt_clean and "68 million" in prompt_clean and "136" not in prompt_clean:
            # Emulates the model deciding to perform math using the calculator tool
            response_text = (
                "Thought: The population of France is 68 million. Now I need to multiply this number by 2.\n"
                "Action: calculator(\"68000000 * 2\")"
            )
        # Step 3 of ReAct: If the calculator result (136000000) has been appended to the prompt context
        elif "68000000 * 2" in prompt_clean and "136000000" in prompt_clean:
            # Emulates the model formulating the final human-readable answer to conclude the loop
            response_text = (
                "Thought: I have the final calculated value of 136,000,000.\n"
                "Final Answer: The population of France multiplied by 2 is 136,000,000."
            )
        # Simple query branch: Returns static text for the France capital check
        elif "capital of france" in prompt_clean:
            response_text = "The capital of France is Paris."
        # Simple query branch: Returns static text for the quantum computing check
        elif "explain quantum computing" in prompt_clean:
            response_text = (
                "Quantum computing is a type of computation that harnesses the collective properties "
                "of quantum states, such as superposition, interference, and entanglement, to perform calculations."
            )
        # Fallback branch: Returns a default response containing a snippet of the input prompt
        else:
            response_text = (
                f"This is a default response from the local Mock LLM. "
                f"Your prompt was: '{prompt[:50]}...'"
            )

        # Estimates output token count based on response string character length (approx 4 chars per token)
        completion_tokens: int = max(1, len(response_text) // 4)

        # Packs response variables into a structured response object
        return MockLLMResponse(
            text=response_text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )


class OllamaLLMClient:
    """
    Integrates with a locally deployed Ollama API endpoint.
    Enables local-first inference using open-source models (e.g. Llama3, Qwen).
    """
    model_name: str
    base_url: str

    def __init__(self, model_name: str = "qwen2.5:0.5b", base_url: str = "http://localhost:11434") -> None:
        """
        Initializes the client connection parameters.

        Args:
            model_name (str): The target Ollama model name to pull and execute.
            base_url (str): Endpoint location of the Ollama system service.
        """
        self.model_name = model_name
        self.base_url = base_url

    def generate(self, prompt: str) -> MockLLMResponse:
        """
        Sends a request to the Ollama HTTP API endpoint to perform model generation.
        
        Args:
            prompt (str): The input prompt string.

        Returns:
            MockLLMResponse: Parsed generation text, costs, and token evaluations.

        Raises:
            RuntimeError: If the remote endpoint is unreachable or returns an error response.
            
        Production-Readiness Considerations:
            1. Retry Policy: Real systems should wrap HTTP calls with tenacity or a similar library to handle transient failures.
            2. Circuit Breaking: Prevent overloading a lagging model server if failure rates spike above a configured threshold.
            3. Client Connection Pool: Avoid reopening TCP connections per inference using persistent sessions (requests.Session()).
            4. Semantic Caching: Cache common prompt templates using redis or database caches to reduce inference overhead.
        """
        import requests

        url: str = f"{self.base_url}/api/generate"
        payload: Dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Connection pooling note: In production, reuse a requests.Session() to optimize TCP handshakes.
            response = requests.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            
            response_text: str = data.get("response", "")
            
            # Extract actual token evaluations if returned, otherwise fallback to character heuristics
            prompt_tokens: int = data.get("prompt_eval_count", max(1, len(prompt) // 4))
            completion_tokens: int = data.get("eval_count", max(1, len(response_text) // 4))
            
            return MockLLMResponse(
                text=response_text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )
        except requests.exceptions.RequestException as re:
            # Detailed operational warning for troubleshooting local deployments
            raise RuntimeError(
                f"Connection to Ollama endpoint failed: {re}. "
                f"Ensure Ollama daemon is active (run: ollama serve) and model '{self.model_name}' "
                f"is downloaded (run: ollama pull {self.model_name})."
            ) from re
        except Exception as e:
            raise RuntimeError(f"Failed to process Ollama response: {e}") from e
