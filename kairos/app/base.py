from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from .models import UserInput, EvaluationResult, LLMProvider
from .mcp_node import MCPToolManager

class LLMClient(ABC):
    def __init__(self, llm_model_name: str, temperature: float = 0.1, **kwargs):
        self.llm_model_name = llm_model_name
        self.temperature = temperature
        self.mcp_manager: List[MCPToolManager] = [None, None]
        self.playwright_config_path = str("./kairos/playwright.config.yml")
        
        self.config = kwargs
    
    async def initialize_mcp(self, thread_id: Optional[int] = None):
        """Initialize MCP tool manager"""
        try:
            self.mcp_manager[thread_id] = MCPToolManager()
            await self.mcp_manager[thread_id].load_from_config(self.playwright_config_path)
        except Exception as e:
            print(f"Warning: Failed to initialize MCP: {e}")
            self.mcp_manager = None
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod 
    async def create_test_plan(self, user_query: str, html_content: str) -> str:
        """Create a test plan for the application"""
        pass
    
    @abstractmethod
    async def run_evaluation_with_tools(self, evaluation_prompt: str, thread_id: Optional[int] = None) -> str:
        """Run evaluation using MCP tools"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Clean up resources"""
        pass
    
    @property
    def provider(self) -> LLMProvider:
        """Return the provider type"""
        return self._provider
    
    @property
    @abstractmethod
    def _provider(self) -> LLMProvider:
        """Abstract property to be implemented by subclasses"""
        pass
    
    
    