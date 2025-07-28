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
    llm_model_name: Optional[str] = None  # Renamed from model_name
    temperature: float = 0.1

class TestResult(BaseModel):
    test_feature: str
    description: str
    actions: str
    assertions: str
    passed: bool
    error_message: Optional[str] = None

class EvaluationResult(BaseModel):
    evaluation_type: EvaluationType
    provider_used: LLMProvider
    success: bool
    # test_results: List[TestResult] = []
    # qualitative_feedback: Optional[str] = None
    execution_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    