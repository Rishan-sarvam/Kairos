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

### Usage as a Server

Run Kairos as a FastAPI server using the command line:

```bash
python3 kairos.server
```

The server will be available at `http://localhost:8000` with the following endpoints:

**Feature Correctness Evaluation:**
```bash
curl -X POST http://localhost:8000/evaluation/feature-test \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Test the login functionality", "url": "https://your-app.com"}'
```

**Qualitative Evaluation:**
```bash
curl -X POST http://localhost:8000/evaluation/qualitative \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Evaluate the user experience", "url": "https://your-app.com"}'
```

### Usage as Streamlit

Launch the web interface for interactive evaluation:

```bash
streamlit run streamlit.py
```

The interface will be available at `http://localhost:8501` and provides:
- Interactive evaluation configuration
- Real-time progress tracking
- Result visualization and download options
