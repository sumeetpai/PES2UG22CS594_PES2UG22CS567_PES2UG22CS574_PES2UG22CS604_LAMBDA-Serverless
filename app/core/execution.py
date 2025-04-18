import os
import json
import tempfile
import subprocess
import logging
import time
import psutil
from typing import Any, Dict, Tuple
from app.models.function import Language, Runtime

logger = logging.getLogger(__name__)

class FunctionExecutionEngine:
    def __init__(self):
        self.temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    def _wrap_code(self, code: str, language: Language) -> str:
        if language == Language.PYTHON:
            indented_code = '\n'.join('    ' + line for line in code.split('\n'))
            return f'''import json
import sys
import signal
import time

def handler(input_data):
{indented_code}

def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)

try:
    with open('/app/input.json', 'r') as f:
        input_data = json.load(f)

    result = handler(input_data)

    if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
        result = str(result)

    with open('/app/output.json', 'w') as f:
        json.dump({{"output": result}}, f)
except Exception as e:
    with open('/app/output.json', 'w') as f:
        json.dump({{"error": str(e)}}, f)
'''
        else:
            indented_code = '\n'.join('    ' + line for line in code.split('\n'))
            return f'''const fs = require('fs');

function handler(input_data) {{
{indented_code}
}}

module.exports = {{ handler }};

const inputData = JSON.parse(fs.readFileSync('/app/input.json', 'utf8'));

try {{
    const result = handler(inputData);
    const output = typeof result === 'object' ? result : {{ output: result }};
    fs.writeFileSync('/app/output.json', JSON.stringify(output));
}} catch (error) {{
    fs.writeFileSync('/app/output.json', JSON.stringify({{ error: error.message }}));
}}
'''

    def execute(self, function_id: int, code: str, language: Language, input_data: Dict[str, Any], runtime: Runtime = Runtime.DOCKER) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as function_file, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:

                json.dump(input_data, input_file)
                input_file.flush()

                wrapped_code = self._wrap_code(code, language)
                function_file.write(wrapped_code)
                function_file.flush()

                start_time = time.time()
                self._run_container(function_file.name, input_file.name, output_file.name, language, runtime)
                end_time = time.time()

                with open(output_file.name, 'r') as f:
                    output = json.load(f)

                try:
                    os.unlink(function_file.name)
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)
                except:
                    pass

                execution_time = round(end_time - start_time, 4)

                memory_used = self._get_container_memory_usage()

                metrics = {
                    "execution_time": execution_time,
                    "memory_used": memory_used,
                    "error": output.get("error")
                }

                return output, metrics

        except Exception as e:
            raise Exception(f"Failed to execute function: {str(e)}")

    def _run_container(self, function_file: str, input_file: str, output_file: str, language: Language, runtime: Runtime) -> None:
        try:
            subprocess.run(['docker', 'info'], check=True, capture_output=True)

            runtime_arg = '--runtime=runsc' if runtime == Runtime.GVISOR else ''
            docker_cmd = [
                'docker', 'run',
                '--memory', '30m',
                '--network', 'none',
            ]
            if runtime_arg:
                docker_cmd.append(runtime_arg)
            docker_cmd += [
                '-v', f'{function_file}:/app/function.js' if language == Language.JAVASCRIPT else f'{function_file}:/app/function.py',
                '-v', f'{input_file}:/app/input.json',
                '-v', f'{output_file}:/app/output.json',
                f'function-{language}-base',
                'node' if language == Language.JAVASCRIPT else 'python',
                '/app/run.js' if language == Language.JAVASCRIPT else '/app/function.py'
            ]

            result = subprocess.run(docker_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Container execution failed: {result.stderr}")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Docker is not running: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to execute container: {str(e)}")

    def _get_container_memory_usage(self) -> float:
        try:
            # Simulate placeholder for actual memory usage capture
            # Real implementation would inspect container stats
            return round(psutil.virtual_memory().used / (1024 * 1024), 2)  # In MB
        except Exception:
            return 0.0
