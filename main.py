from fastapi import FastAPI
from pydantic import BaseModel
from planner import Planner
from orchestrator import Orchestrator

app = FastAPI(title="Mini Agent Orchestrator")
planner = Planner()
orchestrator = Orchestrator()

class ProcessRequest(BaseModel):
    text: str

@app.get("/")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/process")
async def process_request(request: ProcessRequest):
    """
    Core orchestrator endpoint. 
    Accepts text, uses Planner to create a plan, and Orchestrator to execute it.
    """
    plan = planner.parse_request(request.text)
    result = await orchestrator.execute_plan(plan)
    
    # Exposing internal thoughts via "logs" array
    return {
        "text": request.text,
        "plan": plan,
        "logs": result.get("logs", []),
        "orchestrator_result": result
    }
