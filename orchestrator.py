import logging
import tools

# Set up standard python logging
logger = logging.getLogger("orchestrator")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class Orchestrator:
    def __init__(self):
        """Map strings representing tools to actual the python functions."""
        self.tool_map = {
            "cancel_order": tools.cancel_order,
            "send_email": tools.send_email
        }
    
    async def execute_plan(self, plan: list[dict]) -> dict:
        results = []
        execution_logs = []
        
        def log_event(msg: str):
            """Helper to emit local logger events and append to our returned log payload."""
            logger.info(msg)
            execution_logs.append(msg)
            
        num_steps = len(plan)
        log_event(f"Plan received with {num_steps} steps.")
        
        # If the Planner returned an empty plan
        if not plan:
            return {
                "status": "success",
                "message": "Empty plan provided. No actions taken.",
                "results": [],
                "logs": execution_logs
            }
            
        for step_idx, task in enumerate(plan):
            tool_name = task.get("tool")
            params = task.get("params", {})
            
            log_event(f"Executing step: {tool_name}...")
            
            if tool_name not in self.tool_map:
                msg = f"Unknown tool requested: {tool_name}"
                logger.error(msg)
                execution_logs.append(msg)
                return {
                    "status": "failed",
                    "error": msg,
                    "failed_step": step_idx,
                    "logs": execution_logs
                }
                
            tool_func = self.tool_map[tool_name]
            
            # Execute the respective tool
            try:
                # Dynamically passing parameters as kwargs
                step_result = await tool_func(**params)
            except Exception as e:
                msg = f"Exception executing {tool_name}: {str(e)}"
                logger.error(msg)
                execution_logs.append(msg)
                return {
                    "status": "failed",
                    "error": msg,
                    "failed_step": step_idx,
                    "logs": execution_logs
                }
                
            results.append({
                "tool": tool_name,
                "result": step_result
            })
            
            # Guardrail: stop immediately if any step fails
            if step_result.get("status") == "failed":
                log_event("Step failed. Activating guardrail and halting.")
                return {
                    "status": "failed",
                    "error": f"Execution halted due to failure in step: {tool_name}",
                    "failed_step": step_idx,
                    "step_error": step_result.get("error", "Unknown error"),
                    "partial_results": results,
                    "logs": execution_logs
                }
                
        return {
            "status": "success",
            "message": "All steps executed successfully.",
            "results": results,
            "logs": execution_logs
        }
