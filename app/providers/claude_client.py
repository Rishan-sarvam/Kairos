import json
import tempfile
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np

from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from anthropic import AnthropicVertex
from pydantic import BaseModel, Field, create_model

from ..base import LLMClient
from ..models import LLMProvider
from ..mcp_node import MCPToolManager
import os
import dotenv

dotenv.load_dotenv()
model_name = os.getenv("MODEL_NAME")
location = os.getenv("LOCATION")
project_id = os.getenv("PROJECT_ID")

# Configuration constants
MAX_LLM_TOKENS = 4096
MEMORY_WINDOW_K = 6
MAX_TOOL_CHARS = 16000

# Optional Anthropic imports for content normalization
try:
    from anthropic.types import TextContent, ImageContent
except ImportError:
    TextContent = None
    ImageContent = None

class ClaudeClient(LLMClient):
    def __init__(self, model_name: str = model_name,    
                 location: str = location, project_id: str = project_id,
                 temperature: float = 0.1, **kwargs):
        super().__init__(model_name, temperature, **kwargs)
        self.location = location
        self.project_id = project_id
        self._tmp_paths: List[str] = []
        
        # Initialize Anthropic client for direct API calls
        self.anthropic_client = AnthropicVertex(
            region=self.location, 
            project_id=self.project_id
        )
        
        # Initialize LangChain client for agent workflows
        self.langchain_client = ChatAnthropicVertex(
            location=self.location,
            project_id=self.project_id,
            model_name=self.llm_model_name,
            max_tokens=MAX_LLM_TOKENS,
        )
    
    @property
    def _provider(self) -> LLMProvider:
        return LLMProvider.CLAUDE_VERTEX
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a basic response using Anthropic client"""
        try:
            response = self.anthropic_client.messages.create(
                model=self.llm_model_name,  
                max_tokens=kwargs.get("max_tokens", 8192),
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def create_test_plan(self, user_query: str, html_content: str) -> str:
        """Create a playwright test plan for the application"""
        try:
            prompt = f"""Create a comprehensive Playwright test plan for this web application.

USER QUERY: {user_query}

HTML CODE:
{html_content}

Please provide a detailed test plan that includes:
1. Test case descriptions
2. Specific Playwright selectors and actions
3. **IMPORTANT**: Assertions to verify functionality. The assertions should include all the functionalitites of that particular test. Try to find deeper assertions.
4. Make sure there are no duplicate assertions or redundant tests.
5. Expected behaviors

Output your response in this exact JSON format:

```json
[
    {{
        "Test_feature": "name of the test feature",
        "Description": "description of the test feature", 
        "Actions": "list of actions to be performed to test the feature",
        "Assertions": "comprehensive list of assertions to be performed to test the feature"
    }}
]
```

Make sure to wrap the JSON with ```json and ``` code blocks."""

            response = self.anthropic_client.messages.create(
                model=self.llm_model_name,
                max_tokens=8192,
                temperature=0.3,
                system=prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Failed to create test plan: {str(e)}")
    
    async def run_evaluation_with_tools(self, evaluation_prompt: str, thread_id: Optional[int] = None) -> str:
        """Run evaluation using MCP tools and LangChain agent"""

        await self.initialize_mcp(thread_id)
        
        if not self.mcp_manager[thread_id]:
            raise Exception("MCP manager not initialized")
        
        try:
            # Convert MCP tools to LangChain StructuredTools
            lc_tools: List[StructuredTool] = [
                self._wrap_mcp_tool(tname, tmeta, thread_id)
                for tname, tmeta in self.mcp_manager[thread_id].return_documentation().items()
            ]
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an advanced assistant with tool‑use."),
                MessagesPlaceholder("history"),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ])
            
            # Create memory
            memory = ConversationBufferWindowMemory(
                k=MEMORY_WINDOW_K,
                return_messages=True,
                memory_key="history",
            )
            
            # Create agent and executor
            agent = create_tool_calling_agent(
                llm=self.langchain_client, 
                tools=lc_tools, 
                prompt=prompt
            )
            executor = AgentExecutor(
                agent=agent,
                tools=lc_tools,
                memory=memory,
                verbose=True,
                max_iterations=50,
            )
            
            # Run evaluation
            result = await executor.ainvoke({"input": evaluation_prompt})

            await self.cleanup(thread_id)  
            return result["output"]
            
        except Exception as e:
            raise Exception(f"Failed to run evaluation with tools: {str(e)}")
    
    
    def _wrap_mcp_tool(self, name: str, meta: Dict[str, Any], thread_id: Optional[int] = None) -> StructuredTool:
        ArgsModel = self._schema_to_model(name, meta["parameters_dict"])

        async def _arun(**kwargs):
            success, out = await self.mcp_manager[thread_id].call_tool(name, kwargs)
            if not success:
                raise RuntimeError(out["error"])
            out_json = json.dumps(self._normalise(out), default=self._json_safe)
            return self._truncate(out_json)

        return StructuredTool.from_function(
            name         = name,
            description  = meta["documentation"],
            args_schema  = ArgsModel,
            coroutine    = _arun,
            return_direct=False,
        )
    
    def _schema_to_model(self, tool_name: str, schema: Dict[str, Any]) -> type[BaseModel]:
        """Convert MCP JSON‑Schema → Pydantic model."""
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        _tmap = {"string": str, "number": float, "integer": int,
                 "boolean": bool, "array": list, "object": dict}
        fields: Dict[str, tuple] = {}
        
        for pname, pschema in props.items():
            ptype = _tmap.get(pschema.get("type", "string"), str)
            default = ... if pname in required else None
            fields[pname] = (ptype, Field(default, description=pschema.get("description", "")))
        
        return create_model(f"{tool_name}_Args", **fields)
    
    def _normalise(self, obj: Any) -> Any:
        """Recursively turn Anthropic blocks & exotic types into JSON‑safe values."""
        if TextContent and isinstance(obj, TextContent):
            return obj.text
        if ImageContent and isinstance(obj, ImageContent):
            url = getattr(obj, "url", None)
            if url:
                return {"type": "image", "url": url}
            data = getattr(obj, "data", None)
            if data:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                tmp.write(data)
                tmp.close()
                self._tmp_paths.append(tmp.name)
                return {"type": "image", "path": tmp.name}
            return str(obj)

        if isinstance(obj, (Path, bytes, bytearray)):
            return str(obj)
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        if isinstance(obj, dict):
            return {k: self._normalise(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set)):
            return [self._normalise(v) for v in obj]

        return obj
    
    def _json_safe(self, o):
        """Fallback JSON encoder."""
        return str(o)
    
    def _truncate(self, text: str, limit: int = MAX_TOOL_CHARS) -> str:
        """Simple character‑based truncation to keep tool output small."""
        return text if len(text) <= limit else text[:limit] + "… [truncated]"
    
    async def cleanup(self, thread_id: Optional[int] = None):
        """Clean up resources including temp files"""
        await self.mcp_manager[thread_id].cleanup()
        for p in self._tmp_paths:
            try:
                os.unlink(p)
            except FileNotFoundError:
                pass
        self._tmp_paths.clear()
