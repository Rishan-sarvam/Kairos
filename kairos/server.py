from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from kairos.app.models import UserInput, EvaluationResult, EvaluationType, LLMProvider
from kairos.app.providers import create_llm_client
from kairos.app.evaluator import Evaluator

app = FastAPI(title="MCP Evaluator API", description="Web Application Evaluation API using MCP tools")

# Legacy request model for backwards compatibility
class EvalReq(BaseModel):
    user_query: str
    url: str
    provider: LLMProvider = LLMProvider.CLAUDE_VERTEX
    temperature: float = 0.1

@app.get("/")
def root():
    return {
        "message": "Web App Evaluation API", 
        "status": "running",
        "version": "1.0"
    }

@app.post("/evaluation/feature-test")  # Legacy endpoint - quantitative / full test-plan
async def feature_test(req: EvalReq):
    """Legacy endpoint for feature correctness evaluation"""
    try:
        # Convert legacy request to UserInput
        user_input = UserInput(
            user_query=req.user_query,
            app_url=req.url,
            evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
            provider=req.provider or LLMProvider.CLAUDE_VERTEX,
            temperature=req.temperature
        )
        
        llm_client = create_llm_client(user_input)
        evaluator = Evaluator(llm_client)
        result = await evaluator.evaluate(user_input)
        
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
            provider=req.provider or LLMProvider.CLAUDE_VERTEX,
            temperature=req.temperature
        )

        llm_client = create_llm_client(user_input)
        evaluator = Evaluator(llm_client)
        result = await evaluator.evaluate(user_input)
        
        return {"result": result.qualitative_feedback or result.error_message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qualitative evaluation failed: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MCP Evaluator API",
        "version": "1.0"
    }


def main():
    """Main entry point for running the server"""
    import uvicorn
    uvicorn.run("kairos.server:app", host="0.0.0.0", port=8000, reload=True)

# Local dev runner
if __name__ == "__main__":
    main()