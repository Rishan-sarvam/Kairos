# MCP Evaluator Architecture

A modular web application evaluation system that integrates with MCP (Model Context Protocol) tools for comprehensive testing using Playwright.

## Architecture Overview

The system follows a clean, modular architecture:

1. **Input Layer**: Receives input via FastAPI endpoints with Pydantic models
2. **Factory Layer**: Creates appropriate LLM client based on provider
3. **Provider Layer**: Implements different LLM providers (OpenAI, Anthropic, Claude Vertex)
4. **Evaluator Layer**: Orchestrates evaluation logic and MCP tool usage
5. **Output Layer**: Returns structured evaluation results

## Key Components

### Models (`models.py`)
- `UserInput`: Input validation with provider, evaluation type, and configuration
- `EvaluationResult`: Structured output with test results and metadata
- `TestResult`: Individual test case results
- `LLMProvider`: Enum for supported providers
- `EvaluationType`: Enum for evaluation types

### Base Classes (`base.py`)
- `LLMClient`: Abstract base class with MCP integration support
- Common interface for all providers

### Providers (`providers/`)
- `ClaudeClient`: Anthropic Claude via Vertex AI with full MCP support
- `AnthropicClient`: Direct Anthropic API integration
- `OpenAIClient`: OpenAI GPT models integration
- Factory method for client creation

### Evaluator (`evaluator.py`)
- Orchestrates evaluation workflow
- Handles test plan creation and execution
- Supports parallel execution for large test suites
- Parses and structures results

### Server (`server.py`)
- FastAPI endpoints with modern and legacy compatibility
- Comprehensive error handling
- Provider information endpoints

## Supported Features

### LLM Providers
- **Claude Vertex** (Recommended): Full MCP tool integration with Playwright
- **Anthropic**: Direct API access, basic evaluation
- **OpenAI**: GPT models, basic evaluation

### Evaluation Types
- **Feature Correctness**: Creates test plans and executes them with assertions
- **Qualitative**: UX/UI evaluation with detailed feedback

### MCP Integration
- Automatic MCP tool discovery and conversion to LangChain tools
- Playwright browser automation
- Parallel test execution for performance

## API Endpoints

### Main Endpoint
```http
POST /evaluate
```
Full-featured evaluation with complete configuration:
```json
{
    "user_query": "A portfolio website for a potter",
    "app_url": "https://example.com",
    "provider": "claude_vertex",
    "evaluation_type": "feature_correctness",
    "model_name": "claude-sonnet-4@20250514",
    "temperature": 0.1
}
```

### Legacy Endpoints
- `POST /evaluation/feature-test`: Feature correctness (backwards compatible)
- `POST /evaluation/qualitative`: Qualitative evaluation (backwards compatible)

### Utility Endpoints
- `GET /`: API information and available endpoints
- `GET /health`: Health check
- `GET /providers`: List supported providers and capabilities

## Usage Examples

### Basic Usage
```python
from app.models import UserInput, LLMProvider, EvaluationType
from app.providers import create_llm_client
from app.evaluator import Evaluator

# Create input
user_input = UserInput(
    user_query="Test this portfolio website",
    app_url="https://example.com",
    provider=LLMProvider.CLAUDE_VERTEX,
    evaluation_type=EvaluationType.FEATURE_CORRECTNESS
)

# Create client and evaluator
llm_client = create_llm_client(user_input)
evaluator = Evaluator(llm_client)

# Run evaluation
result = await evaluator.evaluate(user_input)
```

### FastAPI Server
```python
# Start the server
uvicorn app.server:app --reload

# Make requests
curl -X POST "http://localhost:8000/evaluate" \
     -H "Content-Type: application/json" \
     -d '{
       "user_query": "Portfolio website",
       "app_url": "https://example.com",
       "provider": "claude_vertex"
     }'
```

## Configuration

### MCP Configuration (`config.yml`)
```yaml
defaults:
  python_env_path: "python"
  node_command: "node"

servers:
  - name: "playwright"
    type: "node"
    path: "../playwright-mcp/index.js"
    env:
      PLAYWRIGHT_BROWSERS_PATH: ""
    args: []
```

### Environment Variables
- `ANTHROPIC_API_KEY`: For direct Anthropic API access
- `OPENAI_API_KEY`: For OpenAI API access
- `GOOGLE_APPLICATION_CREDENTIALS`: For Vertex AI authentication

## Response Format

### Feature Correctness Result
```json
{
    "evaluation_type": "feature_correctness",
    "provider_used": "claude_vertex",
    "success": true,
    "test_results": [
        {
            "test_feature": "Navigation Menu",
            "description": "Test main navigation functionality",
            "actions": "Click menu items, verify navigation",
            "assertions": "Menu opens, links work, pages load",
            "passed": true,
            "error_message": null
        }
    ],
    "execution_time_seconds": 45.2,
    "raw_response": {...}
}
```

### Qualitative Result
```json
{
    "evaluation_type": "qualitative",
    "provider_used": "claude_vertex",
    "success": true,
    "qualitative_feedback": "Detailed UX/UI feedback...",
    "execution_time_seconds": 15.8
}
```

## Development

### Running the Server
```bash
cd app
python server.py
# or
uvicorn server:app --reload
```

### Running Examples
```bash
cd app
python example_usage.py
```

### Testing
Run the example script to verify all components work correctly.

## Migration from Legacy Code

The new architecture maintains backward compatibility with existing endpoints while providing enhanced functionality:

- Legacy `/evaluation/feature-test` and `/evaluation/qualitative` endpoints still work
- New `/evaluate` endpoint provides full configuration options
- All responses include detailed metadata and structured results
- Error handling is more robust and informative

## Performance Features

- **Parallel Execution**: Large test suites are automatically split and run in parallel
- **Memory Management**: Conversation buffers prevent context overflow
- **Resource Cleanup**: Automatic cleanup of temporary files and MCP connections
- **Timeout Protection**: Built-in timeouts for network requests and evaluations

## Extending the System

### Adding New Providers
1. Create a new client class inheriting from `LLMClient`
2. Implement required abstract methods
3. Add to the factory method in `providers/__init__.py`
4. Update the `LLMProvider` enum

### Adding New Evaluation Types
1. Add to `EvaluationType` enum
2. Implement evaluation logic in `Evaluator`
3. Update API documentation and examples 