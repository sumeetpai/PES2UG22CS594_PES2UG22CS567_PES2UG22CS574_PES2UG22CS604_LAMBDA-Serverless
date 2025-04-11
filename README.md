# Serverless Function Execution Platform

A serverless function execution platform built with FastAPI, Docker, and MySQL. This platform allows you to execute user-defined functions in isolated Docker containers with resource limits and timeout enforcement.

## Features

- Execute Python and JavaScript functions in isolated Docker containers
- Resource limits (memory, CPU)
- Timeout enforcement
- Network isolation
- Automatic cleanup of containers and temporary files
- RESTful API for function management

## Prerequisites

- Python 3.9+
- Docker
- MySQL
- Node.js (for JavaScript function support)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd serverless-lambda
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Build Docker images:
```bash
.\build_docker_images.ps1
```

4. Create the database and tables:
```bash
python create_db.py
```

5. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Usage

### Create a Function

```bash
POST http://localhost:8000/functions/
Content-Type: application/json

{
    "name": "hello_world",
    "code": "return f'Hello, {input_data[\"name\"]}!'",
    "language": "python",
    "timeout": 30,
    "memory_limit": 128
}
```

### Execute a Function

```bash
POST http://localhost:8000/functions/{function_id}/execute
Content-Type: application/json

{
    "input": {
        "name": "Alice"
    }
}
```

## Project Structure

```
serverless_lambda/
├── app/
│   ├── api/
│   │   └── functions.py
│   ├── core/
│   │   └── execution.py
│   ├── models/
│   │   └── function.py
│   ├── schemas/
│   │   └── function.py
│   └── main.py
├── docker/
│   ├── python/
│   │   └── run.py
│   └── node/
│       └── run.js
├── requirements.txt
├── create_db.py
└── build_docker_images.ps1
```

## License

MIT