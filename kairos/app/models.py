from pydantic import BaseModel
from enum import Enum
from typing import Dict, List, Optional, Any

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    CLAUDE_VERTEX = "claude_vertex"

class EvaluationType(str, Enum):
    QUALITATIVE = "qualitative"
    FEATURE_CORRECTNESS = "feature_correctness"

class UserInput(BaseModel):
    user_query: str
    app_url: str
    provider: LLMProvider = LLMProvider.CLAUDE_VERTEX
    evaluation_type: EvaluationType = EvaluationType.FEATURE_CORRECTNESS
    llm_model_name: Optional[str] = None
    temperature: float = 0.1

class EvaluationResult(BaseModel):
    evaluation_type: EvaluationType
    provider_used: LLMProvider
    success: bool
    execution_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    