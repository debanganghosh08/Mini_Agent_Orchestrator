import re

class Planner:
    def parse_request(self, user_input: str) -> list[dict]:
        """
        Parses the user input to generate a list of task objects (a Plan).
        Returns a list of dicts like:
        [
            {"tool": "cancel_order", "params": {"order_id": "9921"}},
            {"tool": "send_email", "params": {"email": "user@ex.com", "message": "Order 9921 cancelled"}}
        ]
        """
        plan = []
        user_input_lower = user_input.lower()
        
        # Parse for order cancellation using regex
        # Allow any words between "cancel" and "order"
        order_match = re.search(r"cancel.*?order.*?#?(\d+)", user_input_lower)
        
        # Parse for email using regex
        # Allow any words between "email" and the actual address
        email_match = re.search(r"email.*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", user_input_lower)
        
        # Parse for message strings
        message_match = re.search(r"say(?:ing)?\s+[\"']?(.*?)[\"']?(?:\.|$| and)", user_input_lower)
        
        order_id = order_match.group(1) if order_match else None
        email = email_match.group(1) if email_match else None
        
        # The logic is independent—ensure it doesn't crash if one piece is missing
        if order_id:
            plan.append({
                "tool": "cancel_order",
                "params": {"order_id": order_id}
            })
            
        if email:
            message = message_match.group(1) if message_match else None
            if not message and order_id:
                message = f"Order {order_id} cancelled"
            elif not message:
                message = "Status update regarding your request."
                
            plan.append({
                "tool": "send_email",
                "params": {
                    "email": email,
                    "message": message
                }
            })
            
        return plan
