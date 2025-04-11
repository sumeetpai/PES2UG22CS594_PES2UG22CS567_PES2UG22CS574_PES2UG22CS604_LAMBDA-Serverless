import os
import json
import tempfile
import subprocess
import logging
from typing import Any, Dict
from app.models.function import Language

logger = logging.getLogger(__name__)

class FunctionExecutionEngine:
    def __init__(self):
        self.temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    def _wrap_code(self, code: str, language: Language) -> str:
        if language == Language.PYTHON:
            # Ensure the code is properly indented
            indented_code = '\n'.join('    ' + line for line in code.split('\n'))
            return f'''import json
import sys
import signal
import time

def handler(input_data):
{indented_code}

def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

# Set timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 seconds timeout

try:
    # Read input from file
    with open('/app/input.json', 'r') as f:
        input_data = json.load(f)
    
    # Execute function
    result = handler(input_data)
    
    # Ensure result is JSON serializable
    if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
        result = str(result)
    
    # Write output
    with open('/app/output.json', 'w') as f:
        json.dump({{"output": result}}, f)
except Exception as e:
    with open('/app/output.json', 'w') as f:
        json.dump({{"error": str(e)}}, f)
'''
        else:  # JavaScript
            # Ensure the code is properly indented
            indented_code = '\n'.join('    ' + line for line in code.split('\n'))
            return f'''const fs = require('fs');

// Define the handler function
const handler = function(input_data) {{
{indented_code}
}};

// Read input from file
const inputData = JSON.parse(fs.readFileSync('/app/input.json', 'utf8'));

try {{
    // Execute function
    const result = handler(inputData);
    
    // Ensure result is JSON serializable
    const output = typeof result === 'object' ? result : {{ output: result }};
    
    // Write output
    fs.writeFileSync('/app/output.json', JSON.stringify(output));
}} catch (error) {{
    fs.writeFileSync('/app/output.json', JSON.stringify({{ error: error.message }}));
}}
'''

    def execute(self, function_id: int, code: str, language: Language, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', dir=self.temp_dir, delete=False) as py_file, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.js', dir=self.temp_dir, delete=False) as js_file, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=self.temp_dir, delete=False) as input_file, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=self.temp_dir, delete=False) as output_file:
                
                # Write input data
                json.dump(input_data, input_file)
                input_file.flush()
                
                # Write function code
                wrapped_code = self._wrap_code(code, language)
                if language == Language.PYTHON:
                    py_file.write(wrapped_code)
                    py_file.flush()
                    function_file = py_file.name
                else:  # JavaScript
                    js_file.write(wrapped_code)
                    js_file.flush()
                    function_file = js_file.name
                
                # Build Docker command
                docker_cmd = [
                    "docker", "run",
                    "--memory", "128m",
                    "--network", "none",
                    "-v", f"{function_file}:/app/function.{'py' if language == Language.PYTHON else 'js'}",
                    "-v", f"{input_file.name}:/app/input.json",
                    "-v", f"{output_file.name}:/app/output.json",
                    f"function-{language}-base",
                    "python" if language == Language.PYTHON else "node",
                    f"/app/function.{'py' if language == Language.PYTHON else 'js'}"
                ]
                
                # Execute container
                result = subprocess.run(docker_cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise Exception(f"Container execution failed: {result.stderr}")
                
                # Read output
                with open(output_file.name, 'r') as f:
                    output = json.load(f)
                
                if "error" in output:
                    raise Exception(output["error"])
                
                return output.get("output", None)
                
        except Exception as e:
            logger.error(f"Error executing function {function_id}: {str(e)}")
            raise
        finally:
            # Cleanup
            try:
                os.unlink(function_file)
                os.unlink(input_file.name)
                os.unlink(output_file.name)
            except:
                pass

    def _run_container(self, function_file: str, input_file: str, output_file: str, language: Language) -> None:
        """Run the function in a Docker container."""
        try:
            # Check if Docker is running
            subprocess.run(['docker', 'info'], check=True, capture_output=True)
            
            # Build the Docker command
            docker_cmd = [
                'docker', 'run',
                '--rm',
                '--memory', '30m',
                '--network', 'none',
                '-v', f'{function_file}:/app/function.{language}',
                '-v', f'{input_file}:/app/input.json',
                '-v', f'{output_file}:/app/output.json',
                f'function-{language}-base',
                'node' if language == Language.JAVASCRIPT else 'python',
                f'/app/function.{language}'
            ]
            
            # Run the container
            result = subprocess.run(docker_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Container execution failed: {result.stderr}")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Docker is not running: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to execute container: {str(e)}") 