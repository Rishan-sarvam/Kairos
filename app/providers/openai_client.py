# import asyncio
# from typing import Optional
# from openai import AsyncOpenAI

# from ..base import LLMClient
# from ..models import LLMProvider
# from ..prompts import test_plan_prompt

# class OpenAIClient(LLMClient):
#     def __init__(self, model_name: str = "gpt-4", 
#                  api_key: Optional[str] = None, temperature: float = 0.1, **kwargs):
#         super().__init__(model_name, temperature, **kwargs)
#         self.client = AsyncOpenAI(api_key=api_key)
    
#     @property
#     def _provider(self) -> LLMProvider:
#         return LLMProvider.OPENAI
    
#     async def generate_response(self, prompt: str, **kwargs) -> str:
#         """Generate a basic response using OpenAI client"""
#         try:
#             response = await self.client.chat.completions.create(
#                 model=self.model_name,
#                 max_tokens=kwargs.get("max_tokens", 3000),
#                 temperature=self.temperature,
#                 messages=[{"role": "user", "content": prompt}]
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             raise Exception(f"Failed to generate response: {str(e)}")
    
#     async def create_test_plan(self, user_query: str, html_content: str) -> str:
#         """Create a playwright test plan for the application"""
#         try:
#             system_prompt = test_plan_prompt
#             user_prompt = f"""Create a comprehensive Playwright test plan for this web application.

# USER QUERY: {user_query}

# HTML CODE:
# {html_content}

# Please provide a detailed test plan that includes:
# 1. Test case descriptions
# 2. Specific Playwright selectors and actions
# 3. **IMPORTANT**: Assertions to verify functionality. The assertions should include all the functionalitites of that particular test. Try to find deeper assertions.
# 4. Make sure there are no duplicate assertions or redundant tests.
# 5. Expected behaviors

# Output your response in this exact JSON format:

# ```json
# [
#     {{
#         "Test_feature": "name of the test feature",
#         "Description": "description of the test feature", 
#         "Actions": "list of actions to be performed to test the feature",
#         "Assertions": "comprehensive list of assertions to be performed to test the feature"
#     }}
# ]
# ```

# Make sure to wrap the JSON with ```json and ``` code blocks."""

#             response = await self.client.chat.completions.create(
#                 model=self.model_name,
#                 max_tokens=3000,
#                 temperature=0.3,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ]
#             )
            
#             return response.choices[0].message.content
#         except Exception as e:
#             raise Exception(f"Failed to create test plan: {str(e)}")
    
#     async def run_evaluation_with_tools(self, evaluation_prompt: str) -> str:
#         """Run evaluation - basic implementation without tools for now"""
#         # Note: This is a simplified implementation
#         # For full MCP integration, would need LangChain setup similar to ClaudeClient
#         try:
#             return await self.generate_response(evaluation_prompt)
#         except Exception as e:
#             raise Exception(f"Failed to run evaluation: {str(e)}")
