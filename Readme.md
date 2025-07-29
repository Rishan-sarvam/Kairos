# Kairos - Web Application Evaluation System

## Introduction

Kairos is a comprehensive web application evaluation system that provides automated testing capabilities using Playwright browser automation and Claude Sonnet 4 for intelligent analysis. The system can be used as a Python package, deployed as a server, or run through a user-friendly Streamlit interface.

## Usage

### Set Environment Variables

Before using Kairos, set up the required environment variables:

```bash
export MODEL_NAME="gcp-vertext-model-to-be-loaded"
export LOCATION="gcp-region"
export PROJECT_ID="gcp-project-id"
```

### Usage as a Package

Import and use Kairos directly in your Python code:

```python
from app.evaluator import WebAppEvaluator

evaluator = WebAppEvaluator()
result = evaluator.evaluate_feature_correctness(
    user_query="Test the login functionality",
    url="https://your-app.com"
)
print(result)
```

### Usage as a Server

Run Kairos as a FastAPI server:

```bash
python server.py
```

The server will be available at `http://localhost:8000` with the following endpoints:
- `POST /feature-test` - Feature correctness evaluation

### Usage as Streamlit

Launch the web interface for interactive evaluation:

```bash
# Option 1: Using the launcher script
python kairos.py

# Option 2: Direct Streamlit command
streamlit run streamlit.py
```

The interface will be available at `http://localhost:8501` and provides:
- Interactive evaluation configuration
- Real-time progress tracking
- Result visualization and download options
