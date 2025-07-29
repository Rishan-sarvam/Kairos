import sys
from pathlib import Path
import asyncio
from app.models import UserInput, LLMProvider, EvaluationType
from app.providers import create_llm_client
from app.evaluator import Evaluator

app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

# async def qualitative_evaluation(user_query: str, app_url: str, provider: LLMProvider = LLMProvider.CLAUDE_VERTEX, temperature: float = 0.1):
#     """Run Qualitative evaluation"""
#     print("🔍 Running Qualitative Evaluation...")
    
#     user_input = UserInput(
#         user_query=user_query,
#         app_url=app_url,
#         provider=provider,
#         evaluation_type=EvaluationType.QUALITATIVE,
#         temperature=temperature
#     )
    
#     llm_client = create_llm_client(user_input)
#     evaluator = Evaluator(llm_client)
#     result = await evaluator.evaluate(user_input)
    
#     return result

# async def feature_correctness_evaluation(user_query: str, app_url: str, provider: LLMProvider = LLMProvider.CLAUDE_VERTEX, temperature: float = 0.1):
#     """Run Feature Correctness evaluation"""
#     print("🧪 Running Feature Correctness Evaluation...")
    
#     user_input = UserInput(
#         user_query=user_query,
#         app_url=app_url,
#         provider=provider,
#         evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
#         temperature=temperature
#     )
    
#     llm_client = create_llm_client(user_input)
#     evaluator = Evaluator(llm_client)
#     result = await evaluator.evaluate(user_input)

#     return result

async def run_evaluation(
    user_query: str,
    app_url: str,
    provider: LLMProvider = LLMProvider.CLAUDE_VERTEX,
    evaluation_type: str = "qualitative",
    temperature: float = 0.1
):
    """Run Feature Correctness evaluation"""
    print("🧪 Running Evaluation...")
    
    if evaluation_type == "qualitative":
        eval_type = EvaluationType.QUALITATIVE
    elif evaluation_type == "feature_correctness":
        eval_type = EvaluationType.FEATURE_CORRECTNESS
    else:
        raise ValueError(f"Invalid evaluation type: {evaluation_type}")
    
    user_input = UserInput(
        user_query=user_query,
        app_url=app_url,
        provider=provider,
        evaluation_type=eval_type,
        temperature=temperature
    )
    
    llm_client = create_llm_client(user_input)
    evaluator = Evaluator(llm_client)
    result = await evaluator.evaluate(user_input)

    return result

async def main():
    """Run all examples"""
    print("🚀 MCP Evaluator Architecture Examples\n")

    result = await run_evaluation(
        user_query="A portfolio website for a potter showcasing their work",
        app_url="https://storage.googleapis.com/sarvam-dash-pockets-test/c0123c8e-82ce-4840-9186-3610a85d6969/index.html",
        provider=LLMProvider.CLAUDE_VERTEX,
        temperature=0.1
    )
    print(f"✅ Success: {result.success}")
    print(f"🤖 Provider: {result.provider_used}")
    print(f"⏱️ Time: {result.execution_time_seconds:.2f}s")
    print(f"🧪 Test Results: {result.raw_response}")

if __name__ == "__main__":
    asyncio.run(main()) 