"""
Example usage of the new MCP Evaluator architecture
"""
import sys
import os
from pathlib import Path

# Add the app directory to Python path so relative imports work
app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

import asyncio
from app.models import UserInput, LLMProvider, EvaluationType
from app.providers import create_llm_client
from app.evaluator import Evaluator

async def example_qualitative_evaluation():
    """Example of running a qualitative evaluation"""
    print("🔍 Running Qualitative Evaluation Example...")
    
    # Create user input
    user_input = UserInput(
        user_query="I'd like to create a user interface for an AI tutoring app that allows the user the student to get tutoring on specific subjects. So for example, you know, I will have daily homework assignments. That are available for students to go through. For example, the homework assignments would would be for language arts, math, social studies, and science. So allow the student to basically select the specific subject they would like to do the homework And then within the chat interface, the user the student, be able to go back and forth with the AI 2 to for admins, you know, create Something where For each day and, subject the admin can insert what's the homework? Along with any resources Like, books.",
        app_url="https://storage.googleapis.com/sarvam-dash-pockets-test/cc850d6b-b97f-46e5-a9d5-10d4ecca9012/index.html",
        provider=LLMProvider.CLAUDE_VERTEX,
        evaluation_type=EvaluationType.QUALITATIVE,
        temperature=0.1
    )
    
    # Create LLM client
    llm_client = create_llm_client(user_input)
    print(f"🤖 Provider: {llm_client.provider}")
    
    # Create evaluator
    evaluator = Evaluator(llm_client)
    print(f"🤖 Evaluator: {evaluator}")
    # Run evaluation
    result = await evaluator.evaluate(user_input)
    
    # Print results
    print(f"✅ Success: {result.success}")
    print(f"🤖 Provider: {result.provider_used}")
    print(f"⏱️ Time: {result.execution_time_seconds:.2f}s")
    print(f"🧪 Test Results: {result.raw_response}")
    # if result.qualitative_feedback:
    #     print(f"📝 Feedback: {result.qualitative_feedback[:200]}...")
    if result.error_message:
        print(f"❌ Error: {result.error_message}")

async def example_feature_correctness_evaluation():
    """Example of running a feature correctness evaluation"""
    print("🧪 Running Feature Correctness Evaluation Example...")
    
    # Create user input
    user_input = UserInput(
        user_query="A portfolio website for a potter showcasing their work",
        app_url="https://storage.googleapis.com/sarvam-dash-pockets-test/c0123c8e-82ce-4840-9186-3610a85d6969/index.html",
        provider=LLMProvider.CLAUDE_VERTEX,
        evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
        temperature=0.1
    )
    
    # Create LLM client
    llm_client = create_llm_client(user_input)
    
    # Create evaluator
    evaluator = Evaluator(llm_client)
    
    # Run evaluation
    result = await evaluator.evaluate(user_input)
    
    # Print results
    print(f"✅ Success: {result.success}")
    print(f"🤖 Provider: {result.provider_used}")
    print(f"⏱️ Time: {result.execution_time_seconds:.2f}s")
    print(f"error message: {result.error_message}")
    print(f"🧪 Test Results: {result.raw_response}")
    # print(f"🧪 Test Results: {len(result.test_results)} tests")
    
    # for i, test in enumerate(result.test_results[:3]):  # Show first 3 tests
        # status = "✅ PASS" if test.passed else "❌ FAIL"
        # print(f"  {i+1}. {test.test_feature}: {status}")
        # if test.error_message:
        #     print(f"     Error: {test.error_message}")

async def example_different_providers():
    """Example of using different LLM providers"""
    print("🔄 Testing Different Providers...")
    
    providers = [
        (LLMProvider.CLAUDE_VERTEX, "claude-sonnet-4@20250514")
        # (LLMProvider.ANTHROPIC, "claude-3-sonnet-20240229"),
        # (LLMProvider.OPENAI, "gpt-4")
    ]
    
    for provider, model in providers:
        print(f"\n🤖 Testing {provider} with {model}")
        
        user_input = UserInput(
            user_query="Simple portfolio website evaluation",
            app_url="https://example.com",
            provider=provider,
            llm_model_name=model,
            evaluation_type=EvaluationType.QUALITATIVE,
            temperature=0.1
        )
        
        try:
            llm_client = create_llm_client(user_input)
            print(f"✅ {provider} client created successfully")
            print(f"   Provider: {llm_client.provider}")
            print(f"   Model: {llm_client.llm_model_name}")
            # print(f"   MCP Available: {llm_client.mcp_manager is not None}")
        except Exception as e:
            print(f"❌ Failed to create {provider} client: {e}")

async def main():
    """Run all examples"""
    print("🚀 MCP Evaluator Architecture Examples\n")
    
    # Test different providers
    await example_different_providers()
    
    print("\n" + "="*50 + "\n")
    
    # Test qualitative evaluation
    # await example_qualitative_evaluation()
    
    # print("\n" + "="*50 + "\n")
    
    # # Test feature correctness evaluation
    await example_feature_correctness_evaluation()

if __name__ == "__main__":
    asyncio.run(main()) 