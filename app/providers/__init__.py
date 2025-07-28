from .claude_client import ClaudeClient
from .anthropic_client import AnthropicClient
# from .openai_client import OpenAIClient
from ..models import LLMProvider, UserInput
from ..base import LLMClient

def create_llm_client(user_input: UserInput) -> LLMClient:
    """Factory method to create appropriate LLM client based on provider"""
    
    provider = user_input.provider
    model_name = user_input.llm_model_name
    temperature = user_input.temperature
    
    if provider == LLMProvider.CLAUDE_VERTEX:
        return ClaudeClient(
            model_name=model_name or "claude-sonnet-4@20250514",
            temperature=temperature
        )
    elif provider == LLMProvider.ANTHROPIC:
        return AnthropicClient(
            model_name=model_name or "claude-3-sonnet-20240229",
            temperature=temperature
        )
    # elif provider == LLMProvider.OPENAI:
    #     return OpenAIClient(
    #         model_name=model_name or "gpt-4",
    #         temperature=temperature
    #     )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

__all__ = ["ClaudeClient", "AnthropicClient", "OpenAIClient", "create_llm_client"]
