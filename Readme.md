# Web Application Evaluation API

This evaluation system provides comprehensive automated testing capabilities for web applications using Playwright browser automation. The API offers two distinct evaluation approaches to assess different aspects of web application quality.

## Overview

The evaluation system uses:
- **Playwright MCP (Model Context Protocol)** for browser automation
- **Claude Sonnet 4** for intelligent test generation and analysis
- **FastAPI** for REST API endpoints
- **Containerized deployment** with official Playwright Docker image

## API Endpoints

### 1. Feature Test API - `/feature-test`

**Purpose**: Comprehensive functional testing

**Method**: `POST`

**Methodology**: 
Functional testing of web applications by:
1. **Test Plan Creation**: The input taken is the user query and the url. From the url, the index.html file is extracted to get a good knowledge of the elements present in the application that can be tested.
2. **Dynamic Test Plan Generation**: Creates comprehensive Playwright test plans based on user requirements and discovered UI elements. 
3. **Assertions**: Importance is given to deep assertions based on features and elements. **These assertions are the ones that capture the flaws of any feature**
3. **Testing using the PLaywright MCP**: Use Claude Sonnet 4 integrated with the playwright MCP to iteratively interact with a headless browser to execute the tests mentioned in the test plan. 

**Request Format**:
```json
{
  "user_query": "Description of the application functionality/requirements",
  "url": "https://example.com/your-app"
}
```

**Response Format**:
```json
{
  "result": {
    "application_evaluation": {
      "features_analysis": [
        {
          "feature_name": "Feature Name",
          "status": "SUCCESS|FAILURE|PARTIAL_SUCCESS",
          "reason": "Detailed explanation of test results"
        }
      ],
      "overall_summary": {
        "failed_features": "7",
        "overall_status": "PASS|FAIL",
        "key_issues": ["Critical issues discovered"],
        "recommendations": ["Specific improvement suggestions"]
      }
    }
  }
}
```

**Use Cases**:
- Bug identification 
- Regression testing after updates
- Feature completeness validation
- Accessibility and interaction testing

## Deployment

The evaluation system is containerized and deployed using:
- **Base Image**: `mcr.microsoft.com/playwright:v1.40.0-jammy`
- **Cloud Platform**: Google Cloud Run
- **Authentication**: Google Cloud IAM with JWT tokens
- **Configuration**: YAML-based MCP server configuration

For deployment details, refer to the included Dockerfile and configuration files.

## 🔧 Technical Requirements


### Request Headers
```
Content-Type: application/json
Authorization: Bearer <token>
```


## 🛠️ Integration Examples

### Python Integration
```python
import requests

# Feature testing
feature_response = requests.post(
    "https://your-api-endpoint/feature-test",
    headers={
        "Authorization": "Bearer your-token",
        "Content-Type": "application/json"
    },
    json={
        "user_query": "E-commerce checkout flow",
        "url": "https://your-app.com"
    }
)

# Qualitative evaluation  
qualitative_response = requests.post(
    "https://your-api-endpoint/evaluation/qualitative",
    headers={
        "Authorization": "Bearer your-token", 
        "Content-Type": "application/json"
    },
    json={
        "user_query": "Online shopping platform for mobile users",
        "url": "https://your-app.com"
    }
)
```

### cURL Examples
```bash
# Feature Test
curl -X POST "https://your-api-endpoint/feature-test" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "Task management application",
    "url": "https://your-app.com"
  }'

# Qualitative Evaluation  
curl -X POST "https://your-api-endpoint/evaluation/qualitative" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "Productivity app for remote teams", 
    "url": "https://your-app.com"
  }'
```

## 🖥️ Web UI Interface

In addition to the API endpoints, the evaluation framework now includes a user-friendly web interface built with Streamlit.

### Features

- **Intuitive Interface**: Clean, modern UI with sidebar navigation
- **Evaluation Type Selection**: Dropdown to choose between Feature Correctness and Qualitative Evaluation
- **Real-time Results**: Live progress indicators and result display
- **Result Management**: View, download, and manage evaluation results
- **Input Validation**: Built-in URL and query validation

### Running the UI

You can launch the web interface in two ways:

#### Option 1: Using the launcher script (Recommended)
```bash
python run_ui.py
```

#### Option 2: Direct Streamlit command
```bash
streamlit run streamlit.py
```

### Accessing the Interface

Once started, the UI will be available at:
- **Local URL**: http://localhost:8501
- The interface will automatically open in your default web browser

### Using the Interface

1. **Select Evaluation Type**: Use the sidebar dropdown to choose between:
   - **Feature Correctness**: Detailed functional testing with Playwright
   - **Qualitative Evaluation**: Comprehensive quality assessment

2. **Configure Evaluation**: 
   - Enter your user query describing the application
   - Provide the URL of the web application to test

3. **Run Evaluation**: Click "Run Evaluation" to start the process

4. **View Results**: Results are displayed with options to:
   - View formatted JSON output
   - Download results as JSON files
   - Manage multiple evaluation sessions

### UI Benefits

- **No API tokens required** for local development
- **Interactive result exploration** with expandable sections
- **Session persistence** to track multiple evaluations
- **Export capabilities** for result sharing and documentation
