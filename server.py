from typing import Any
from mcp.server.fastmcp import FastMCP
from langchain_community.llms import Ollama

mcp = FastMCP("code-generation")

code_llm = Ollama(model="mistral")

@mcp.tool()
async def generate_mcp_code(query: str) -> str:
    """
    Takes a natural-language spec (e.g. “Generate an MCP server with X tools…”)
    and returns a complete Python file as text.
    """
    # Directly ask the LLM to complete the spec-to-code prompt:
    prompt = f"""You are an expert Python developer. 
    Generate a complete MCP server implementation, based on the following spec:
    {query}
    """
    # `apredict` returns the text of the first completion.
    code = await code_llm.apredict(text=prompt)
    return code

if __name__ == "__main__":
    mcp.run(transport="stdio")