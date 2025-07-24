from mcp.server.fastmcp import FastMCP
from langchain_ollama import OllamaLLM
from pathlib import Path
import os

MODEL_NAME = os.getenv("MODEL_NAME")

mcp = FastMCP(name="code-generation", host="0.0.0.0")

code_llm = OllamaLLM(model=MODEL_NAME, base_url="http://ollama:11434", temperature=0.3)

DOC_PATH = Path("mcp_documentation.txt")
MCP_DOC = DOC_PATH.read_text(encoding="utf-8").strip()

DOC_PATH = Path("llms-small.txt")
MCP_LLMS_SMALL_DOC = DOC_PATH.read_text(encoding="utf-8").strip()


@mcp.tool()
async def get_doc() -> str:
    """Return the full MCP (Model Context Protocol) documentation."""
    return MCP_DOC


@mcp.tool()
async def generate_mcp_client_server_code(query: str) -> str:
    """
    Takes a natural-language specification of required tools and returns a complete Python file as text which should be returned to the user as-is.

    Args:
        query: A natural-language specification of the MCP (Model Context Protocol) server and/or client and what needs to be implemented.
    """

    prompt = f"""You are an expert Python developer.
    Depending on the user request generate a complete MCP (Model Context Protocol) server or MCP (Model Context Protocol) client implementation, based on the following spec:
    <query>
    {query}
    </query>
    
    The documentation for MCP (Model Context Protocol) is:
    <documentation>
    {MCP_LLMS_SMALL_DOC}
    </documentation>
    
    Align with the 'Implementation example' from the documentation! Stick to the example implementations as much as possible.
    """
    code = await code_llm.ainvoke(input=prompt)

    return code


if __name__ == "__main__":

    mcp.run(transport="sse")
