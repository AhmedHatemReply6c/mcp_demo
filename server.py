from typing import Any
from mcp.server.fastmcp import FastMCP
from langchain_community.llms import Ollama
from pathlib import Path

mcp = FastMCP("code-generation")

code_llm = Ollama(model="mistral")
DOC_PATH = Path(__file__).parent / "mcp_documentation.txt"
MCP_DOC  = DOC_PATH.read_text(encoding="utf-8").strip()

@mcp.tool()
async def generate_mcp_code(query: str) -> str:
    """
    Takes a natural-language spec (e.g. “Generate an MCP server with X tools…”)
    and returns a complete Python file as text.
    """
    prompt = f"""You are an expert Python developer.
    Generate a complete MCP server implementation, based on the following spec:
    {query}
    The documentation for MCP is:
    {MCP_DOC}
    """

    code = await code_llm.apredict(text=prompt)
    return code

if __name__ == "__main__":
    mcp.run(transport="stdio")