import sys
from pathlib import Path
import asyncio
from kairos.app.models import UserInput, LLMProvider, EvaluationType
from kairos.app.providers import create_llm_client
from kairos.app.evaluator import Evaluator

async def run_evaluation(
    user_query: str,
    app_url: str,
    provider: str,
    evaluation_type: str = "qualitative",
    temperature: float = 0.1
):
    """Run Feature Correctness evaluation"""
    print("🧪 Running Evaluation...")

    if provider == "claude-vertex":
        llm_provider = LLMProvider.CLAUDE_VERTEX
    elif provider == "openai":
        llm_provider = LLMProvider.OPENAI
    elif provider == "anthropic":
        llm_provider = LLMProvider.ANTHROPIC
    else:
        raise ValueError(f"Invalid provider: {provider}")
    
    if evaluation_type == "qualitative":
        eval_type = EvaluationType.QUALITATIVE
    elif evaluation_type == "feature_correctness":
        eval_type = EvaluationType.FEATURE_CORRECTNESS
    else:
        raise ValueError(f"Invalid evaluation type: {evaluation_type}")
    
    user_input = UserInput(
        user_query=user_query,
        app_url=app_url,
        provider=llm_provider,
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