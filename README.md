# Serverless Function Execution Platform

A powerful platform for executing serverless functions with support for multiple runtimes (Docker and gVisor) and languages (Python and JavaScript). This platform provides a user-friendly interface for creating, executing, and monitoring functions with detailed metrics and performance analysis.

## Features

### Function Management
- Create and deploy functions in Python or JavaScript
- Execute functions with custom inputs
- Delete functions when no longer needed
- View function execution history and metrics

### Runtime Support
- Docker runtime for traditional container execution
- gVisor runtime for enhanced security
- Performance comparison between runtimes
- Metrics dashboard for runtime analysis

### Language Support
- Python functions with full standard library access
- JavaScript functions with modern ES6+ features
- Example functions in both languages
- Language-specific input handling

### Metrics and Analytics
- Execution time tracking
- Memory usage monitoring
- Success rate analysis
- Error tracking and reporting
- Runtime comparison metrics
- Performance visualization

### User Interface
- Streamlit-based web interface
- Interactive function creation
- Dynamic input forms
- Real-time execution results
- Comprehensive metrics dashboard

## Getting Started

### Prerequisites
- Python 3.8+
- Docker
- gVisor (for gVisor runtime)
- Node.js (for JavaScript functions)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/serverless-function-platform.git
cd serverless-function-platform
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload
```

4. Start the frontend:
```bash
streamlit run frontend.py
```

### Example Functions

The platform comes with several example functions:

#### Hello World
- Python: Simple greeting function
- JavaScript: Template literal-based greeting
- Input: `{"name": "Bob"}`
- Output: `"Hello, Bob!"`

#### Calculator
- Python: Basic arithmetic operations
- JavaScript: Switch-based calculator
- Input: `{"operation": "add", "num1": 10, "num2": 5}`
- Output: `15`

#### Fibonacci
- Python: Recursive Fibonacci implementation
- JavaScript: ES6 Fibonacci function
- Input: `{"n": 10}`
- Output: `55`

#### String Manipulation
- Python: String operations (reverse, case, length)
- JavaScript: String methods with template literals
- Input: `{"text": "Hello World", "operation": "uppercase"}`
- Output: `"HELLO WORLD"`

#### JSON Processing
- Python: JSON data operations
- JavaScript: Object methods for JSON handling
- Input: `{"data": {"name": "John", "age": 30}, "operation": "keys"}`
- Output: `["name", "age"]`

#### Array Operations
- JavaScript: Array manipulation functions
- Input: `{"array": [1, 5, 3, 9, 2], "operation": "sum"}`
- Output: `20`

#### Date Formatting
- JavaScript: Date formatting utilities
- Input: `{"date": "2023-01-15T12:30:45Z", "format": "locale"}`
- Output: Formatted date string

## Usage

### Creating a Function
1. Navigate to "Create Function" in the sidebar
2. Choose an example function or write your own
3. Select language (Python/JavaScript)
4. Choose runtime (Docker/gVisor)
5. Set timeout and memory limits
6. Click "Create Function"

### Executing a Function
1. Go to "Execute Function" page
2. Select a function from the dropdown
3. Provide input data in the form
4. Click "Execute Function"
5. View results and metrics

### Viewing Metrics
1. Access "Metrics Dashboard"
2. View execution statistics
3. Compare runtime performance
4. Analyze success rates
5. Monitor resource usage

## Architecture

### Backend
- FastAPI for REST API
- SQLite database for function storage
- Docker/gVisor for function execution
- Metrics collection and analysis

### Frontend
- Streamlit for web interface
- Interactive forms and visualizations
- Real-time updates
- Responsive design

## Performance Comparison

### Docker vs gVisor
- Execution time comparison
- Memory usage analysis
- Success rate metrics
- Error rate comparison
- Resource utilization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the backend framework
- Streamlit for the frontend
- Docker and gVisor for runtime support
- The open-source community for various tools and libraries