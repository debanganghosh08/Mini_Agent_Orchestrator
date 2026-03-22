# 🤖 Mini Agent Orchestrator

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, event-driven agentic workflow engine built with **FastAPI**. This project demonstrates a complete "Brain-to-Action" pipeline using a natural language Planner, an asynchronous Orchestrator, and fail-safe Guardrails.

---

## 📍 Table of Contents
1. [🚀 Project Overview](#-project-overview)
2. [🏗️ System Architecture](#️-system-architecture)
3. [✨ Key Features](#-key-features)
4. [🛠️ File Walkthrough](#️-file-walkthrough)
5. [📥 Getting Started](#-getting-started)
6. [🧪 Testing the Agent](#-testing-the-agent)
7. [📂 Project Structure](#-project-structure)

---

## 🚀 Project Overview
The **Mini Agent Orchestrator** is designed for engineers who build agents that *do work*, not just chat. It solves the challenge of taking a messy natural language request and turning it into a sequence of reliable, asynchronous tool calls. 

**The Scenario:** A user asks to cancel an order and receive an email. The agent must plan the steps, execute them asynchronously, and—most importantly—stop if a critical failure occurs.

---

## 🏗️ System Architecture
The project follows a **Decoupled 3-Tier Design**:



1.  **The Planner (`planner.py`)**: The "Brain." It parses natural language into a structured JSON **Plan**.
2.  **The Orchestrator (`orchestrator.py`)**: The "Engine." It loops through the plan and manages tool execution.
3.  **The Tools (`tools.py`)**: The "Hands." Mocked asynchronous functions that simulate real-world API behavior and latency.

---

## ✨ Key Features
* **⚡ Async-First Design**: Utilizes `asyncio` and `FastAPI` to ensure the server remains non-blocking during 1-second tool simulations.
* **🛡️ Execution Guardrails**: Implements a strict "Circuit Breaker" logic. If `cancel_order` fails (simulated 20% failure rate), the agent halts immediately to prevent sending a false confirmation email.
* **🔍 Agentic Observability**: Surfaces internal "thought" logs directly in the API response, allowing users to trace the agent's decision-making process.
* **🧩 Dynamic Tool Mapping**: Uses a secure `tool_map` to execute function pointers, avoiding dangerous `eval()` calls.

---

## 🛠️ File Walkthrough

| File | Responsibility | Key Technical Highlight |
| :--- | :--- | :--- |
| **`main.py`** | API Gateway | Exposes the `/process` endpoint and aggregates logs for the frontend. |
| **`planner.py`** | NLP Parsing | Uses robust, non-greedy regex (`.*?`) to extract IDs and Emails from "noisy" text. |
| **`orchestrator.py`** | Workflow Logic | Manages the task loop and enforces fail-fast guardrails. |
| **`tools.py`** | Mock Infrastructure | Simulates network latency and statistical failure rates (20%). |

---

## 📥 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/debanganghosh08/Mini_Agent_Orchestrator.git](https://github.com/debanganghosh08/Mini_Agent_Orchestrator.git)
cd Mini_Agent_Orchestrator
```
### 2. Set Up Environment
```bash
# It is recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Run the Server
```bash
uvicorn main:app --reload
```
### 🧪 Testing the Agent
Navigate to ```bash http://127.0.0.1:8000/docs ```
```bash
Open the POST /process endpoint.

Click "Try it out" and use the following JSON:

JSON
{
  "text": "Please cancel my order #9921 and email me the confirmation at user@example.com"
}
Observe the Guardrail: Click "Execute" multiple times. You will see some requests succeed and some fail with a failed_step log, demonstrating the agent's reliability.
```

## 📂 Project Structure
```bash
mini-agent-orchestrator/
├── main.py                # FastAPI Entry Point
├── planner.py             # NLP & Task Planning
├── orchestrator.py        # Execution Engine & Guardrails
├── tools.py               # Async Mock Tools
├── test_tools.py          # Latency & Probability Tests
├── requirements.txt       # Dependencies
└── README.md              # Project Documentation
```
Developed by Debangan Ghosh
Linkedin - https://www.linkedin.com/in/debangan-ghosh/
