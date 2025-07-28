from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

from .models import UserInput, EvaluationResult, EvaluationType, LLMProvider
from .providers import create_llm_client
from .evaluator import Evaluator

app = FastAPI(title="MCP Evaluator API", description="Web Application Evaluation API using MCP tools")

# Legacy request model for backwards compatibility
class EvalReq(BaseModel):
    user_query: str
    url: str

@app.get("/")
def root():
    return {
        "message": "Web App Evaluation API", 
        "status": "running",
        "version": "2.0",
        "endpoints": {
            "POST /evaluate": "Main evaluation endpoint with full configuration",
            "POST /evaluation/feature-test": "Legacy feature correctness evaluation",
            "POST /evaluation/qualitative": "Legacy qualitative evaluation"
        }
    }

@app.post("/evaluate", response_model=EvaluationResult)
async def evaluate(user_input: UserInput):
    """
    Main evaluation endpoint with full configuration support
    
    Supports:
    - Multiple LLM providers (OpenAI, Anthropic, Claude Vertex)
    - Different evaluation types (qualitative, feature_correctness)
    - Custom model names and temperature settings
    """
    try:
        # Create appropriate LLM client
        llm_client = create_llm_client(user_input)
        
        # Create evaluator
        evaluator = Evaluator(llm_client)
        
        # Run evaluation
        result = await evaluator.evaluate(user_input)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.post("/evaluation/feature-test")  # Legacy endpoint - quantitative / full test-plan
async def feature_test(req: EvalReq):
    """Legacy endpoint for feature correctness evaluation"""
    try:
        # Convert legacy request to UserInput
        user_input = UserInput(
            user_query=req.user_query,
            app_url=req.url,
            evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
            provider=LLMProvider.CLAUDE_VERTEX  # Default to Claude for legacy requests
        )
        
        # Create LLM client and evaluator
        llm_client = create_llm_client(user_input)
        evaluator = Evaluator(llm_client)
        
        # Run evaluation
        result = await evaluator.evaluate(user_input)
        
        # Return in legacy format
        return {"result": result.model_dump()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature test failed: {str(e)}")

@app.post("/evaluation/qualitative")  # Legacy endpoint - qualitative-only
async def qualitative(req: EvalReq):
    """Legacy endpoint for qualitative evaluation"""
    try:
        # Convert legacy request to UserInput
        user_input = UserInput(
            user_query=req.user_query,
            app_url=req.url,
            evaluation_type=EvaluationType.QUALITATIVE,
            provider=LLMProvider.CLAUDE_VERTEX  # Default to Claude for legacy requests
        )
        
        # Create LLM client and evaluator
        llm_client = create_llm_client(user_input)
        evaluator = Evaluator(llm_client)
        
        # Run evaluation
        result = await evaluator.evaluate(user_input)
        
        # Return in legacy format
        return {"result": result.qualitative_feedback or result.error_message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qualitative evaluation failed: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MCP Evaluator API",
        "version": "2.0"
    }

@app.get("/providers")
def get_supported_providers():
    """Get list of supported LLM providers"""
    return {
        "providers": [
            {
                "id": LLMProvider.CLAUDE_VERTEX,
                "name": "Claude Vertex",
                "description": "Anthropic Claude via Google Vertex AI",
                "default_model": "claude-sonnet-4@20250514",
                "mcp_support": True
            },
            {
                "id": LLMProvider.ANTHROPIC,
                "name": "Anthropic",
                "description": "Anthropic Claude direct API",
                "default_model": "claude-3-sonnet-20240229",
                "mcp_support": False
            },
            {
                "id": LLMProvider.OPENAI,
                "name": "OpenAI",
                "description": "OpenAI GPT models",
                "default_model": "gpt-4",
                "mcp_support": False
            }
        ]
    }

# Local dev runner
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)