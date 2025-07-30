import asyncio
from kairos import run_evaluation

async def example():
    # Example: Evaluate a portfolio website for a potter
    user_query = "A portfolio website for a potter showcasing their work"
    app_url = "https://storage.googleapis.com/sarvam-dash-pockets-test/c0123c8e-82ce-4840-9186-3610a85d6969/index.html"
    provider = "claude-vertex"
    temperature = 0.1
    evaluation_type = "feature_correctness"  # or "qualitative"

    result = await run_evaluation(
        user_query=user_query,
        app_url=app_url,
        provider=provider,
        evaluation_type=evaluation_type,
        temperature=temperature
    )

    print("=== Evaluation Result ===")
    print(f"Success: {result.success}")
    print(f"Provider Used: {result.provider_used}")
    print(f"Execution Time: {result.execution_time_seconds:.2f}s")
    print(f"Raw Response:\n{result.raw_response}")

if __name__ == "__main__":
    asyncio.run(example())
