# Kairos - An ML-Based Oracle for Web Application Quality and Correctness Evaluation

## Introduction

Kairos is an advanced multi-agent system designed to accelerate the evaluation and improvement of AI-generated web applications. While AI can quickly generate functional web apps, these often exhibit subtle but significant shortcomings—for example, a shopping cart that works but places the "checkout" button in an unexpected location, color schemes that technically meet accessibility standards but clash visually, or multi-step forms that are logically sound yet unintuitive for users. Kairos addresses these challenges by combining automated browser testing with intelligent qualitative analysis, enabling both functional and user experience assessments. Whether used as a Python package, a server, or through an interactive Streamlit interface, Kairos empowers teams to identify, understand, and resolve the nuanced issues that AI-generated apps frequently exhibit.

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
