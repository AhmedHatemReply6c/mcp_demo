from mcp.server.fastmcp import FastMCP
from langchain_ollama import OllamaLLM
from pathlib import Path
import os

MODEL_NAME = os.getenv("MODEL_NAME")

mcp = FastMCP(name="code-generation", host="0.0.0.0")

code_llm = OllamaLLM(model=MODEL_NAME,base_url="http://ollama:11434")

DOC_PATH = Path("mcp_documentation.txt")
MCP_DOC = DOC_PATH.read_text(encoding="utf-8").strip()

DOC_PATH = Path("llms-full.txt")
MCP_LLMS_FULL_DOC = DOC_PATH.read_text(encoding="utf-8").strip()


@mcp.tool()
async def get_doc() -> str:
    """Return the full MCP (Model Context Protocol) documentation."""
    return MCP_DOC


@mcp.tool()
async def generate_mcp_server_code(query: str) -> str:
    """
    Takes a natural-language specification of required tools and returns a complete Python file as text which should be returned to the user as-is.

    Args:
        query: A natural-language specification of the MCP (Model Context Protocol) server and what needs to be implemented.
    """

    prompt = f"""You are an expert Python developer.
    Generate a complete MCP (Model Context Protocol) server implementation, based on the following spec:
    <query>
    {query}
    </query>
    
    The documentation for MCP (Model Context Protocol) is:
    <documentation>
    {MCP_LLMS_FULL_DOC}
    </documentation>
    
    Align with the 'Implementation example' from the documentation!
    """
    code = await code_llm.ainvoke(input=prompt)


    return code


if __name__ == "__main__":

    mcp.run(transport="sse")
