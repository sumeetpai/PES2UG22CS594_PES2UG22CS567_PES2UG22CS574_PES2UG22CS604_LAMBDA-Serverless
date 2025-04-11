import json
import sys
import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

# Set timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 seconds timeout

try:
    # Read input from file
    with open('/app/input.json', 'r') as f:
        input_data = json.load(f)
    
    # Import and execute function
    from function import handler
    result = handler(input_data)
    
    # Ensure result is JSON serializable
    if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
        result = str(result)
    
    # Write output
    with open('/app/output.json', 'w') as f:
        json.dump({"output": result}, f)
except Exception as e:
    with open('/app/output.json', 'w') as f:
        json.dump({"error": str(e)}, f) 