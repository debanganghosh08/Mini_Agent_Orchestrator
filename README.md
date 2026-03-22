# Mini Agent Orchestrator

## Project Overview
The Mini Agent Orchestrator is a lightweight, asynchronous, FastAPI-based framework that simulates natural language AI agent orchestration without relying on paid APIs. By using a regex-based Planner, it maps user intents to executable sequences of mocked tools, executing them with strict guardrail policies.

## Architecture
The framework follows a clean 3-tier design:
1. **Planner (`planner.py`)**: Evaluates natural language inputs using robust regex logic to construct an ordered, structured "Plan" (a sequence of actionable tasks).
2. **Orchestrator (`orchestrator.py`)**: Ingests the plan, dynamically mapping requested actions to Python execution functions. It manages loop execution, context, and immediate failure halts.
3. **Tools (`tools.py`)**: Houses the foundational asynchronous functions (e.g., `cancel_order`, `send_email`). These simulate real network constraints (like 1-second delays) and statistical uncertainty (like a simulated 20% failure rate).

## Key Features
- **Async Execution**: Built natively for asynchronous environments (`asyncio.sleep`, `FastAPI`). This allows concurrent multi-request scaling without blocking the event loop.
- **Fail-Safe Guardrails**: The Orchestrator enforces a strict "stop-on-fail" policy. If any tool task returns a failure state, the sequence instantly halts and propagates the failure metadata backwards—preventing compounding errors.
- **API Transparency Logs**: Internal loop "thoughts" are surfaced straight through the HTTP response via a structured `logs` array, building observability without terminal-scrapping.

## Installation & Usage
1. **Install Dependencies**: Ensure you are using Python 3.9+ and run:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Server**:
   ```bash
   uvicorn main:app --reload
   ```
3. **Usage via Curl or Postman**: Send a POST request to `http://localhost:8000/process`.
   ```json
   {
       "text": "Cancel my order #1234 and email me at test@example.com"
   }
   ```

## Design Choices
### Why a `tool_map`?
The `tool_map` strictly isolates and encapsulates the available commands to the Orchestrator. Instead of running unsafe `eval()` string executions, mapped dictionaries safely reference Python method pointers. This bounds the execution context explicitly to safe, internal APIs.
### Why return a "Plan" instead of Executing Immediately?
Returning a cleanly decoupled Plan enables three critical agentic paradigms: **Auditability** (approving destructive tasks before they fire), **Error Recovery** (knowing exactly where a sequence stopped to resume later), and **Dry Runs** (simulating side effects safely).
