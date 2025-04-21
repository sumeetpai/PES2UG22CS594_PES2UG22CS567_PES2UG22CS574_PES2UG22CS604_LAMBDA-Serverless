import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Constants
API_BASE_URL = "http://localhost:8000/functions"

# Page config
st.set_page_config(
    page_title="Serverless Function Platform",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 Serverless Function Platform")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Functions List", "Create Function", "Execute Function", "Metrics Dashboard"])

# Functions List Page
if page == "Functions List":
    st.header("Functions List")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        functions = response.json()
        
        if functions:
            for func in functions:
                with st.expander(f"📝 {func['name']} (ID: {func['id']})"):
                    st.code(func['code'], language=func['language'])
                    st.write(f"**Language:** {func['language']}")
                    st.write(f"**Runtime:** {func['runtime']}")
                    st.write(f"**Created:** {datetime.fromisoformat(func['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Add delete button
                    if st.button(f"Delete Function", key=f"delete_{func['id']}"):
                        try:
                            delete_response = requests.delete(f"{API_BASE_URL}/{func['id']}")
                            if delete_response.status_code == 200:
                                st.success(f"Function {func['name']} deleted successfully!")
                                st.experimental_rerun()
                            else:
                                st.error(f"Error deleting function: {delete_response.text}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    if func['metrics']:
                        st.write("**Recent Executions:**")
                        metrics_df = pd.DataFrame(func['metrics'])
                        metrics_df['created_at'] = pd.to_datetime(metrics_df['created_at'])
                        metrics_df = metrics_df.sort_values('created_at', ascending=False)
                        
                        # Success rate
                        success_rate = (metrics_df['success'].sum() / len(metrics_df)) * 100
                        st.metric("Success Rate", f"{success_rate:.1f}%")
                        
                        # Execution time chart
                        fig = px.line(metrics_df, x='created_at', y='execution_time',
                                    title='Execution Time Trend')
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No functions found. Create one using the 'Create Function' page.")
            
    except Exception as e:
        st.error(f"Error fetching functions: {str(e)}")

# Create Function Page
elif page == "Create Function":
    st.header("Create New Function")
    
    # Add example functions
    st.subheader("Example Functions")
    example_functions = {
        "Hello World (Python)": {
            "name": "hello_world",
            "code": "return f'Hello, {input_data[\"name\"]}!'",
            "language": "python",
            "runtime": "docker",
            "input_example": '{"name": "Bob"}',
            "description": "A simple greeting function that takes a name and returns a greeting."
        },
        "Hello World (JavaScript)": {
            "name": "hello_world_js",
            "code": "return `Hello, ${input_data.name}!`;",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"name": "Bob"}',
            "description": "A simple greeting function in JavaScript that takes a name and returns a greeting."
        },
        "Hello World_1 (Python)": {
            "name": "hello_world_1",
            "code": "return f'Hello, {input_data[\"name\"]}!'",
            "language": "python",
            "runtime": "gvisor",
            "input_example": '{"name": "Bob"}',
            "description": "A simple greeting function that takes a name and returns a greeting."
        },
        "Hello World_1 (JavaScript)": {
            "name": "hello_world_js_1",
            "code": "return `Hello, ${input_data.name}!`;",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"name": "Bob"}',
            "description": "A simple greeting function in JavaScript that takes a name and returns a greeting."
        },
        "Calculator (Python)": {
            "name": "calculator",
            "code": "operation = input_data.get('operation', 'add')\nnum1 = input_data.get('num1', 0)\nnum2 = input_data.get('num2', 0)\n\nif operation == 'add':\n    return num1 + num2\nelif operation == 'subtract':\n    return num1 - num2\nelif operation == 'multiply':\n    return num1 * num2\nelif operation == 'divide':\n    return num1 / num2 if num2 != 0 else 'Error: Division by zero'\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "docker",
            "input_example": '{"operation": "add", "num1": 10, "num2": 5}',
            "description": "A calculator function that performs basic arithmetic operations."
        },
        "Calculator (JavaScript)": {
            "name": "calculator_js",
            "code": "const operation = input_data.operation || 'add';\nconst num1 = input_data.num1 || 0;\nconst num2 = input_data.num2 || 0;\n\nswitch(operation) {\n  case 'add':\n    return num1 + num2;\n  case 'subtract':\n    return num1 - num2;\n  case 'multiply':\n    return num1 * num2;\n  case 'divide':\n    return num2 !== 0 ? num1 / num2 : 'Error: Division by zero';\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"operation": "add", "num1": 10, "num2": 5}',
            "description": "A calculator function in JavaScript that performs basic arithmetic operations."
        },
        "Calculator_1 (Python)": {
            "name": "calculator_1",
            "code": "operation = input_data.get('operation', 'add')\nnum1 = input_data.get('num1', 0)\nnum2 = input_data.get('num2', 0)\n\nif operation == 'add':\n    return num1 + num2\nelif operation == 'subtract':\n    return num1 - num2\nelif operation == 'multiply':\n    return num1 * num2\nelif operation == 'divide':\n    return num1 / num2 if num2 != 0 else 'Error: Division by zero'\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "gvisor",
            "input_example": '{"operation": "add", "num1": 10, "num2": 5}',
            "description": "A calculator function that performs basic arithmetic operations."
        },
        "Calculator_1 (JavaScript)": {
            "name": "calculator_js_1",
            "code": "const operation = input_data.operation || 'add';\nconst num1 = input_data.num1 || 0;\nconst num2 = input_data.num2 || 0;\n\nswitch(operation) {\n  case 'add':\n    return num1 + num2;\n  case 'subtract':\n    return num1 - num2;\n  case 'multiply':\n    return num1 * num2;\n  case 'divide':\n    return num2 !== 0 ? num1 / num2 : 'Error: Division by zero';\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"operation": "add", "num1": 10, "num2": 5}',
            "description": "A calculator function in JavaScript that performs basic arithmetic operations."
        },
        "Fibonacci (Python)": {
            "name": "fibonacci",
            "code": "def fib(n):\n    if n <= 1:\n        return n\n    else:\n        return fib(n-1) + fib(n-2)\n\nn = input_data.get('n', 10)\nreturn fib(n)",
            "language": "python",
            "runtime": "docker",
            "input_example": '{"n": 10}',
            "description": "Calculates the nth Fibonacci number recursively."
        },
        "Fibonacci (JavaScript)": {
            "name": "fibonacci_js",
            "code": "function fib(n) {\n  if (n <= 1) return n;\n  return fib(n-1) + fib(n-2);\n}\n\nconst n = input_data.n || 10;\nreturn fib(n);",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"n": 10}',
            "description": "Calculates the nth Fibonacci number recursively in JavaScript."
        },
        "Fibonacci_1 (Python)": {
            "name": "fibonacci_1",
            "code": "def fib(n):\n    if n <= 1:\n        return n\n    else:\n        return fib(n-1) + fib(n-2)\n\nn = input_data.get('n', 10)\nreturn fib(n)",
            "language": "python",
            "runtime": "gvisor",
            "input_example": '{"n": 10}',
            "description": "Calculates the nth Fibonacci number recursively."
        },
        "Fibonacci_1 (JavaScript)": {
            "name": "fibonacci_js_1",
            "code": "function fib(n) {\n  if (n <= 1) return n;\n  return fib(n-1) + fib(n-2);\n}\n\nconst n = input_data.n || 10;\nreturn fib(n);",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"n": 10}',
            "description": "Calculates the nth Fibonacci number recursively in JavaScript."
        },
        "String Manipulation (Python)": {
            "name": "string_manipulation",
            "code": "text = input_data.get('text', '')\noperation = input_data.get('operation', 'reverse')\n\nif operation == 'reverse':\n    return text[::-1]\nelif operation == 'uppercase':\n    return text.upper()\nelif operation == 'lowercase':\n    return text.lower()\nelif operation == 'length':\n    return len(text)\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "docker",
            "input_example": '{"text": "Hello World", "operation": "uppercase"}',
            "description": "Performs various string operations like reverse, uppercase, lowercase, and length."
        },
        "String Manipulation (JavaScript)": {
            "name": "string_manipulation_js",
            "code": "const text = input_data.text || '';\nconst operation = input_data.operation || 'reverse';\n\nswitch(operation) {\n  case 'reverse':\n    return text.split('').reverse().join('');\n  case 'uppercase':\n    return text.toUpperCase();\n  case 'lowercase':\n    return text.toLowerCase();\n  case 'length':\n    return text.length;\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"text": "Hello World", "operation": "uppercase"}',
            "description": "Performs various string operations in JavaScript like reverse, uppercase, lowercase, and length."
        },
        "String Manipulation_1 (Python)": {
            "name": "string_manipulation_1",
            "code": "text = input_data.get('text', '')\noperation = input_data.get('operation', 'reverse')\n\nif operation == 'reverse':\n    return text[::-1]\nelif operation == 'uppercase':\n    return text.upper()\nelif operation == 'lowercase':\n    return text.lower()\nelif operation == 'length':\n    return len(text)\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "gvisor",
            "input_example": '{"text": "Hello World", "operation": "uppercase"}',
            "description": "Performs various string operations like reverse, uppercase, lowercase, and length."
        },
        "String Manipulation_1 (JavaScript)": {
            "name": "string_manipulation_js_1",
            "code": "const text = input_data.text || '';\nconst operation = input_data.operation || 'reverse';\n\nswitch(operation) {\n  case 'reverse':\n    return text.split('').reverse().join('');\n  case 'uppercase':\n    return text.toUpperCase();\n  case 'lowercase':\n    return text.toLowerCase();\n  case 'length':\n    return text.length;\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"text": "Hello World", "operation": "uppercase"}',
            "description": "Performs various string operations in JavaScript like reverse, uppercase, lowercase, and length."
        },
        "JSON Processing (Python)": {
            "name": "json_processor",
            "code": "data = input_data.get('data', {})\noperation = input_data.get('operation', 'keys')\n\nif operation == 'keys':\n    return list(data.keys())\nelif operation == 'values':\n    return list(data.values())\nelif operation == 'count':\n    return len(data)\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "docker",
            "input_example": '{"data": {"name": "John", "age": 30, "city": "New York"}, "operation": "keys"}',
            "description": "Processes JSON data to extract keys, values, or count items."
        },
        "JSON Processing (JavaScript)": {
            "name": "json_processor_js",
            "code": "const data = input_data.data || {};\nconst operation = input_data.operation || 'keys';\n\nswitch(operation) {\n  case 'keys':\n    return Object.keys(data);\n  case 'values':\n    return Object.values(data);\n  case 'count':\n    return Object.keys(data).length;\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"data": {"name": "John", "age": 30, "city": "New York"}, "operation": "keys"}',
            "description": "Processes JSON data in JavaScript to extract keys, values, or count items."
        },
        "JSON Processing_1 (Python)": {
            "name": "json_processor_1",
            "code": "data = input_data.get('data', {})\noperation = input_data.get('operation', 'keys')\n\nif operation == 'keys':\n    return list(data.keys())\nelif operation == 'values':\n    return list(data.values())\nelif operation == 'count':\n    return len(data)\nelse:\n    return 'Error: Invalid operation'",
            "language": "python",
            "runtime": "gvisor",
            "input_example": '{"data": {"name": "John", "age": 30, "city": "New York"}, "operation": "keys"}',
            "description": "Processes JSON data to extract keys, values, or count items."
        },
        "JSON Processing_1 (JavaScript)": {
            "name": "json_processor_js_1",
            "code": "const data = input_data.data || {};\nconst operation = input_data.operation || 'keys';\n\nswitch(operation) {\n  case 'keys':\n    return Object.keys(data);\n  case 'values':\n    return Object.values(data);\n  case 'count':\n    return Object.keys(data).length;\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"data": {"name": "John", "age": 30, "city": "New York"}, "operation": "keys"}',
            "description": "Processes JSON data in JavaScript to extract keys, values, or count items."
        },
        "Array Operations (JavaScript)": {
            "name": "array_operations_js",
            "code": "const array = input_data.array || [];\nconst operation = input_data.operation || 'sum';\n\nswitch(operation) {\n  case 'sum':\n    return array.reduce((sum, val) => sum + val, 0);\n  case 'average':\n    return array.length > 0 ? array.reduce((sum, val) => sum + val, 0) / array.length : 0;\n  case 'max':\n    return array.length > 0 ? Math.max(...array) : null;\n  case 'min':\n    return array.length > 0 ? Math.min(...array) : null;\n  case 'sort':\n    return [...array].sort((a, b) => a - b);\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"array": [1, 5, 3, 9, 2, 8, 4, 7, 6], "operation": "sum"}',
            "description": "Performs various array operations in JavaScript like sum, average, max, min, and sort."
        },
        "Array Operations_1 (JavaScript)": {
            "name": "array_operations_js_1",
            "code": "const array = input_data.array || [];\nconst operation = input_data.operation || 'sum';\n\nswitch(operation) {\n  case 'sum':\n    return array.reduce((sum, val) => sum + val, 0);\n  case 'average':\n    return array.length > 0 ? array.reduce((sum, val) => sum + val, 0) / array.length : 0;\n  case 'max':\n    return array.length > 0 ? Math.max(...array) : null;\n  case 'min':\n    return array.length > 0 ? Math.min(...array) : null;\n  case 'sort':\n    return [...array].sort((a, b) => a - b);\n  default:\n    return 'Error: Invalid operation';\n}",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"array": [1, 5, 3, 9, 2, 8, 4, 7, 6], "operation": "sum"}',
            "description": "Performs various array operations in JavaScript like sum, average, max, min, and sort."
        },
        "Date Formatting (JavaScript)": {
            "name": "date_formatting_js",
            "code": "const date = new Date(input_data.date || Date.now());\nconst format = input_data.format || 'iso';\n\nswitch(format) {\n  case 'iso':\n    return date.toISOString();\n  case 'locale':\n    return date.toLocaleDateString();\n  case 'time':\n    return date.toLocaleTimeString();\n  case 'datetime':\n    return date.toLocaleString();\n  case 'unix':\n    return Math.floor(date.getTime() / 1000);\n  default:\n    return 'Error: Invalid format';\n}",
            "language": "javascript",
            "runtime": "docker",
            "input_example": '{"date": "2023-01-15T12:30:45Z", "format": "locale"}',
            "description": "Formats dates in various ways using JavaScript's Date object."
        },
        "Date Formatting_1 (JavaScript)": {
            "name": "date_formatting_js_1",
            "code": "const date = new Date(input_data.date || Date.now());\nconst format = input_data.format || 'iso';\n\nswitch(format) {\n  case 'iso':\n    return date.toISOString();\n  case 'locale':\n    return date.toLocaleDateString();\n  case 'time':\n    return date.toLocaleTimeString();\n  case 'datetime':\n    return date.toLocaleString();\n  case 'unix':\n    return Math.floor(date.getTime() / 1000);\n  default:\n    return 'Error: Invalid format';\n}",
            "language": "javascript",
            "runtime": "gvisor",
            "input_example": '{"date": "2023-01-15T12:30:45Z", "format": "locale"}',
            "description": "Formats dates in various ways using JavaScript's Date object."
        }
    }
    
    example_function = st.selectbox("Select an example function to use as a template", list(example_functions.keys()))
    if example_function:
        example = example_functions[example_function]
        st.write(f"**Description:** {example['description']}")
        st.code(example['code'], language=example['language'])
        st.write(f"**Example Input:**")
        st.code(example['input_example'], language="json")
    
    with st.form("create_function"):
        name = st.text_input("Function Name", value=example_functions[example_function]["name"] if example_function else "")
        code = st.text_area("Function Code", value=example_functions[example_function]["code"] if example_function else "")
        language = st.selectbox("Language", ["python", "javascript"], index=0 if example_function and example_functions[example_function]["language"] == "python" else 1)
        runtime = st.selectbox("Runtime", ["docker", "gvisor"], index=0 if example_function and example_functions[example_function]["runtime"] == "docker" else 1)
        timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=300, value=30)
        memory_limit = st.number_input("Memory Limit (MB)", min_value=64, max_value=1024, value=128)
        
        submitted = st.form_submit_button("Create Function")
        
        if submitted:
            try:
                data = {
                    "name": name,
                    "code": code,
                    "language": language,
                    "runtime": runtime,
                    "timeout": timeout,
                    "memory_limit": memory_limit
                }
                
                response = requests.post(f"{API_BASE_URL}/", json=data)
                if response.status_code == 200:
                    st.success("Function created successfully!")
                else:
                    st.error(f"Error creating function: {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Execute Function Page
elif page == "Execute Function":
    st.header("Execute Function")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        functions = response.json()
        
        if functions:
            function_options = {f"{f['name']} (ID: {f['id']})": f['id'] for f in functions}
            selected_function = st.selectbox("Select Function", list(function_options.keys()))
            function_id = function_options[selected_function]
            
            # Get the selected function details
            selected_func = next((f for f in functions if f['id'] == function_id), None)
            
            if selected_func:
                # Show function details
                st.subheader("Function Details")
                st.code(selected_func['code'], language=selected_func['language'])
                st.write(f"**Language:** {selected_func['language']}")
                st.write(f"**Runtime:** {selected_func['runtime']}")
                
                # Determine input requirements based on function code
                input_requirements = []
                input_example = {}
                
                # Simple pattern matching to detect input requirements
                code = selected_func['code'].lower()
                
                # Check for common input patterns with more variations
                input_patterns = {
                    "name": [
                        r"input_data\[[\"']name[\"']\]",
                        r"input_data\.name",
                        r"input_data\[\"name\"\]",
                        r"input_data\['name'\]"
                    ],
                    "text": [
                        r"input_data\[[\"']text[\"']\]",
                        r"input_data\.text",
                        r"input_data\[\"text\"\]",
                        r"input_data\['text'\]"
                    ],
                    "operation": [
                        r"input_data\[[\"']operation[\"']\]",
                        r"input_data\.operation",
                        r"input_data\[\"operation\"\]",
                        r"input_data\['operation'\]"
                    ],
                    "num1": [
                        r"input_data\[[\"']num1[\"']\]",
                        r"input_data\.num1",
                        r"input_data\[\"num1\"\]",
                        r"input_data\['num1'\]"
                    ],
                    "num2": [
                        r"input_data\[[\"']num2[\"']\]",
                        r"input_data\.num2",
                        r"input_data\[\"num2\"\]",
                        r"input_data\['num2'\]"
                    ],
                    "n": [
                        r"input_data\[[\"']n[\"']\]",
                        r"input_data\.n",
                        r"input_data\[\"n\"\]",
                        r"input_data\['n'\]"
                    ],
                    "data": [
                        r"input_data\[[\"']data[\"']\]",
                        r"input_data\.data",
                        r"input_data\[\"data\"\]",
                        r"input_data\['data'\]"
                    ],
                    "array": [
                        r"input_data\[[\"']array[\"']\]",
                        r"input_data\.array",
                        r"input_data\[\"array\"\]",
                        r"input_data\['array'\]"
                    ],
                    "date": [
                        r"input_data\[[\"']date[\"']\]",
                        r"input_data\.date",
                        r"input_data\[\"date\"\]",
                        r"input_data\['date'\]"
                    ],
                    "format": [
                        r"input_data\[[\"']format[\"']\]",
                        r"input_data\.format",
                        r"input_data\[\"format\"\]",
                        r"input_data\['format'\]"
                    ]
                }
                
                import re
                
                # Check each pattern
                for param, patterns in input_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, code):
                            if param == "name":
                                input_requirements.append("name (string): The name to greet")
                                input_example["name"] = "Bob"
                            elif param == "text":
                                input_requirements.append("text (string): The text to manipulate")
                                input_example["text"] = "Hello World"
                            elif param == "operation":
                                input_requirements.append("operation (string): The operation to perform")
                                input_example["operation"] = "uppercase"
                            elif param == "num1":
                                input_requirements.append("num1 (number): First number for calculation")
                                input_example["num1"] = 10
                            elif param == "num2":
                                input_requirements.append("num2 (number): Second number for calculation")
                                input_example["num2"] = 5
                            elif param == "n":
                                input_requirements.append("n (number): The position in the sequence")
                                input_example["n"] = 10
                            elif param == "data":
                                input_requirements.append("data (object): JSON data to process")
                                input_example["data"] = {"name": "John", "age": 30, "city": "New York"}
                            elif param == "array":
                                input_requirements.append("array (array): Array of numbers to process")
                                input_example["array"] = [1, 5, 3, 9, 2, 8, 4, 7, 6]
                            elif param == "date":
                                input_requirements.append("date (string): Date string to format")
                                input_example["date"] = "2023-01-15T12:30:45Z"
                            elif param == "format":
                                input_requirements.append("format (string): Format to apply")
                                input_example["format"] = "locale"
                            break
                
                # If no patterns found, try to detect from function name
                if not input_requirements:
                    func_name = selected_func['name'].lower()
                    if "hello" in func_name or "greet" in func_name:
                        input_requirements.append("name (string): The name to greet")
                        input_example["name"] = "Bob"
                    elif "calc" in func_name:
                        input_requirements.extend([
                            "operation (string): The operation to perform",
                            "num1 (number): First number",
                            "num2 (number): Second number"
                        ])
                        input_example.update({
                            "operation": "add",
                            "num1": 10,
                            "num2": 5
                        })
                    elif "fib" in func_name:
                        input_requirements.append("n (number): The position in the sequence")
                        input_example["n"] = 10
                    elif "string" in func_name:
                        input_requirements.extend([
                            "text (string): The text to manipulate",
                            "operation (string): The operation to perform"
                        ])
                        input_example.update({
                            "text": "Hello World",
                            "operation": "uppercase"
                        })
                    elif "json" in func_name:
                        input_requirements.extend([
                            "data (object): JSON data to process",
                            "operation (string): The operation to perform"
                        ])
                        input_example.update({
                            "data": {"name": "John", "age": 30, "city": "New York"},
                            "operation": "keys"
                        })
                    elif "array" in func_name:
                        input_requirements.extend([
                            "array (array): Array of numbers to process",
                            "operation (string): The operation to perform"
                        ])
                        input_example.update({
                            "array": [1, 5, 3, 9, 2, 8, 4, 7, 6],
                            "operation": "sum"
                        })
                    elif "date" in func_name:
                        input_requirements.extend([
                            "date (string): Date string to format",
                            "format (string): Format to apply"
                        ])
                        input_example.update({
                            "date": "2023-01-15T12:30:45Z",
                            "format": "locale"
                        })
                
                # Show input requirements
                st.subheader("Input Requirements")
                if input_requirements:
                    for req in input_requirements:
                        st.write(f"- {req}")
                else:
                    st.write("This function doesn't have specific input requirements detected.")
                    st.write("You can use the Advanced JSON Input option below.")
                
                # Show example input
                st.subheader("Example Input")
                st.code(json.dumps(input_example, indent=2), language="json")
                
                # Show how to use the function
                st.subheader("How to Use This Function")
                st.info("""
                ## How to use this function:
                
                1. **Simple Input**: Just provide the values directly:
                ```json
                {}
                ```
                
                2. **Or with the 'input' wrapper** (both work the same):
                ```json
                {{
                    "input": {}
                }}
                ```
                
                The function will receive your input data directly.
                """.format(
                    json.dumps(input_example, indent=2),
                    json.dumps(input_example, indent=2)
                ))
            
            # Create dynamic input form
            st.subheader("Function Input")
            with st.form("function_input_form"):
                input_values = {}
                
                # Create appropriate input fields based on detected requirements
                if "name" in input_example:
                    input_values["name"] = st.text_input("Name", value=input_example["name"])
                
                if "text" in input_example:
                    input_values["text"] = st.text_input("Text", value=input_example["text"])
                
                if "operation" in input_example:
                    if "text" in input_example:
                        operation_options = ["reverse", "uppercase", "lowercase", "length"]
                    elif "data" in input_example:
                        operation_options = ["keys", "values", "count"]
                    elif "array" in input_example:
                        operation_options = ["sum", "average", "max", "min", "sort"]
                    elif "date" in input_example:
                        operation_options = ["iso", "locale", "time", "datetime", "unix"]
                    else:
                        operation_options = ["add", "subtract", "multiply", "divide"]
                    input_values["operation"] = st.selectbox("Operation", operation_options)
                
                if "num1" in input_example:
                    input_values["num1"] = st.number_input("First Number", value=float(input_example["num1"]))
                
                if "num2" in input_example:
                    input_values["num2"] = st.number_input("Second Number", value=float(input_example["num2"]))
                
                if "n" in input_example:
                    input_values["n"] = st.number_input("Position (n)", value=int(input_example["n"]), min_value=0)
                
                if "data" in input_example:
                    data_input = st.text_area("JSON Data", value=json.dumps(input_example["data"], indent=2))
                    try:
                        input_values["data"] = json.loads(data_input)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON data")
                
                if "array" in input_example:
                    array_input = st.text_input("Array (comma-separated numbers)", value=",".join(map(str, input_example["array"])))
                    try:
                        input_values["array"] = [float(x.strip()) for x in array_input.split(",")]
                    except ValueError:
                        st.error("Invalid array input. Please enter comma-separated numbers.")
                
                if "date" in input_example:
                    input_values["date"] = st.text_input("Date", value=input_example["date"])
                
                if "format" in input_example:
                    input_values["format"] = st.selectbox("Format", ["iso", "locale", "time", "datetime", "unix"])
                
                # Submit button
                submitted = st.form_submit_button("Execute Function")
                
                if submitted:
                    try:
                        # Try both direct and wrapped input formats
                        response = requests.post(
                            f"{API_BASE_URL}/{function_id}/execute",
                            json={"input": input_values}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("Execution successful!")
                            st.json(result)
                        else:
                            st.error(f"Execution failed: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Show raw JSON input option
            with st.expander("Advanced: Raw JSON Input"):
                raw_input = st.text_area("Raw JSON Input", value=json.dumps(input_example, indent=2))
                if st.button("Execute with Raw Input"):
                    try:
                        input_json = json.loads(raw_input)
                        response = requests.post(
                            f"{API_BASE_URL}/{function_id}/execute",
                            json={"input": input_json}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("Execution successful!")
                            st.json(result)
                        else:
                            st.error(f"Execution failed: {response.text}")
                            
                    except json.JSONDecodeError:
                        st.error("Invalid JSON input")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info("No functions available to execute")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Metrics Dashboard Page
elif page == "Metrics Dashboard":
    st.header("Metrics Dashboard")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        functions = response.json()
        
        if functions:
            # Collect all metrics
            all_metrics = []
            for func in functions:
                if func['metrics']:
                    for metric in func['metrics']:
                        metric['function_name'] = func['name']
                        metric['runtime'] = func['runtime']
                        all_metrics.append(metric)
            
            if all_metrics:
                metrics_df = pd.DataFrame(all_metrics)
                metrics_df['created_at'] = pd.to_datetime(metrics_df['created_at'])
                
                # Success Rate by Function
                st.subheader("Success Rate by Function")
                success_rate = metrics_df.groupby('function_name')['success'].mean() * 100
                fig = px.bar(success_rate, title='Success Rate by Function')
                st.plotly_chart(fig, use_container_width=True)
                
                # Execution Time Distribution
                st.subheader("Execution Time Distribution")
                fig = px.histogram(metrics_df, x='execution_time', 
                                 title='Execution Time Distribution',
                                 nbins=20)
                st.plotly_chart(fig, use_container_width=True)
                
                # Memory Usage Trend
                st.subheader("Memory Usage Trend")
                fig = px.line(metrics_df, x='created_at', y='memory_used',
                            color='function_name',
                            title='Memory Usage Over Time')
                st.plotly_chart(fig, use_container_width=True)
                
                # Error Analysis
                st.subheader("Error Analysis")
                error_df = metrics_df[metrics_df['error'].notna()]
                if not error_df.empty:
                    error_counts = error_df.groupby('error').size()
                    fig = px.pie(values=error_counts.values, names=error_counts.index,
                               title='Error Distribution')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No errors recorded in the metrics")
                
                # Docker vs gVisor Comparison
                st.subheader("Docker vs gVisor Comparison")
                
                # Check if we have both runtimes
                runtimes = metrics_df['runtime'].unique()
                if 'docker' in runtimes and 'gvisor' in runtimes:
                    # Create tabs for different comparison metrics
                    comparison_tab1, comparison_tab2, comparison_tab3 = st.tabs(["Execution Time", "Memory Usage", "Success Rate"])
                    
                    with comparison_tab1:
                        st.write("### Execution Time Comparison")
                        # Calculate average execution time by runtime
                        exec_time_comparison = metrics_df.groupby('runtime')['execution_time'].agg(['mean', 'std', 'count']).reset_index()
                        exec_time_comparison['mean'] = exec_time_comparison['mean'].round(4)
                        exec_time_comparison['std'] = exec_time_comparison['std'].round(4)
                        
                        # Display as a table
                        st.table(exec_time_comparison)
                        
                        # Create a bar chart
                        fig = px.bar(exec_time_comparison, x='runtime', y='mean', 
                                    error_y='std',
                                    title='Average Execution Time by Runtime',
                                    labels={'mean': 'Average Execution Time (seconds)', 'runtime': 'Runtime'})
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Box plot for distribution
                        fig = px.box(metrics_df, x='runtime', y='execution_time',
                                    title='Execution Time Distribution by Runtime')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with comparison_tab2:
                        st.write("### Memory Usage Comparison")
                        # Calculate average memory usage by runtime
                        memory_comparison = metrics_df.groupby('runtime')['memory_used'].agg(['mean', 'std', 'count']).reset_index()
                        memory_comparison['mean'] = memory_comparison['mean'].round(2)
                        memory_comparison['std'] = memory_comparison['std'].round(2)
                        
                        # Display as a table
                        st.table(memory_comparison)
                        
                        # Create a bar chart
                        fig = px.bar(memory_comparison, x='runtime', y='mean', 
                                    error_y='std',
                                    title='Average Memory Usage by Runtime',
                                    labels={'mean': 'Average Memory Usage (MB)', 'runtime': 'Runtime'})
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Box plot for distribution
                        fig = px.box(metrics_df, x='runtime', y='memory_used',
                                    title='Memory Usage Distribution by Runtime')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with comparison_tab3:
                        st.write("### Success Rate Comparison")
                        # Calculate success rate by runtime
                        success_comparison = metrics_df.groupby('runtime')['success'].agg(['mean', 'count']).reset_index()
                        success_comparison['mean'] = (success_comparison['mean'] * 100).round(2)
                        success_comparison.rename(columns={'mean': 'success_rate'}, inplace=True)
                        
                        # Display as a table
                        st.table(success_comparison)
                        
                        # Create a bar chart
                        fig = px.bar(success_comparison, x='runtime', y='success_rate',
                                    title='Success Rate by Runtime',
                                    labels={'success_rate': 'Success Rate (%)', 'runtime': 'Runtime'})
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Error rate by runtime
                        error_by_runtime = metrics_df[metrics_df['error'].notna()].groupby('runtime').size().reset_index(name='error_count')
                        total_by_runtime = metrics_df.groupby('runtime').size().reset_index(name='total_count')
                        
                        error_by_runtime = error_by_runtime.merge(total_by_runtime, on='runtime')
                        error_by_runtime['error_rate'] = (error_by_runtime['error_count'] / error_by_runtime['total_count'] * 100).round(2)
                        
                        fig = px.bar(error_by_runtime, x='runtime', y='error_rate',
                                    title='Error Rate by Runtime',
                                    labels={'error_rate': 'Error Rate (%)', 'runtime': 'Runtime'})
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Summary insights
                    st.subheader("Summary Insights")
                    
                    # Execution time insights
                    docker_time = exec_time_comparison[exec_time_comparison['runtime'] == 'docker']['mean'].values[0]
                    gvisor_time = exec_time_comparison[exec_time_comparison['runtime'] == 'gvisor']['mean'].values[0]
                    time_diff = abs(docker_time - gvisor_time)
                    time_diff_percent = (time_diff / min(docker_time, gvisor_time) * 100).round(2)
                    
                    if docker_time < gvisor_time:
                        time_insight = f"Docker is {time_diff_percent}% faster than gVisor on average."
                    else:
                        time_insight = f"gVisor is {time_diff_percent}% faster than Docker on average."
                    
                    # Memory usage insights
                    docker_memory = memory_comparison[memory_comparison['runtime'] == 'docker']['mean'].values[0]
                    gvisor_memory = memory_comparison[memory_comparison['runtime'] == 'gvisor']['mean'].values[0]
                    memory_diff = abs(docker_memory - gvisor_memory)
                    memory_diff_percent = (memory_diff / min(docker_memory, gvisor_memory) * 100).round(2)
                    
                    if docker_memory < gvisor_memory:
                        memory_insight = f"Docker uses {memory_diff_percent}% less memory than gVisor on average."
                    else:
                        memory_insight = f"gVisor uses {memory_diff_percent}% less memory than Docker on average."
                    
                    # Success rate insights
                    docker_success = success_comparison[success_comparison['runtime'] == 'docker']['success_rate'].values[0]
                    gvisor_success = success_comparison[success_comparison['runtime'] == 'gvisor']['success_rate'].values[0]
                    success_diff = abs(docker_success - gvisor_success)
                    
                    if docker_success > gvisor_success:
                        success_insight = f"Docker has a {success_diff:.2f}% higher success rate than gVisor."
                    else:
                        success_insight = f"gVisor has a {success_diff:.2f}% higher success rate than Docker."
                    
                    # Display insights
                    st.write(f"**Execution Time:** {time_insight}")
                    st.write(f"**Memory Usage:** {memory_insight}")
                    st.write(f"**Success Rate:** {success_insight}")
                    
                else:
                    st.info("Not enough data to compare Docker and gVisor. Make sure you have functions executed with both runtimes.")
            else:
                st.info("No metrics data available")
        else:
            st.info("No functions found")
            
    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}") 