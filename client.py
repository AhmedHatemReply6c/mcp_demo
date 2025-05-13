import asyncio
from pathlib import Path

from langchain_community.llms import Ollama
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate

# read the snippet at startup
DOC_PATH = Path(__file__).parent / "mcp_documentation.txt"
MCP_DOC = DOC_PATH.read_text(encoding="utf-8").strip()

# 1) Define your system‐level prefix and a suffix template
PREFIX = """\
You are an assistant expert in the MCP framework.
MCP is an open protocol that enables seamless integration between LLM applications and external data sources and tools
Use the MCP documentation to answer any user questions about MCP's concepts, APIs or usage.  
If the user asks you to generate code, ALWAYS delegate to the `generate_code` tool (which routes to a specialized coding server) rather than writing code yourself.\
"""

SUFFIX = """\
User's question:
{input}

{format_instructions}  ← be sure to call the right tool above

Response:
"""

# 2) Combine into one PromptTemplate that LangChain’s zero-shot agent will use
prompt = PromptTemplate(
    input_variables=["input", "format_instructions"],
    template=PREFIX + "\n\n" + SUFFIX,
)

async def main():
    async with Client(PythonStdioTransport("server.py")) as mcp_client:
        llm = Ollama(model="mistral")

        @tool
        async def get_doc(query: str) -> str:
            """Returns the MCP documentation."""
            return MCP_DOC

        @tool
        async def generate_code(query: str) -> str:
            """Routes to a specialized coding agent that generates high-quality MCP code."""
            result = await mcp_client.call_tool("generate_mcp_code", {"query": query})
            print("CODE AGENT OUTPUT " , result)
            return result[0].text

        tools = [get_doc, generate_code]

        agent = initialize_agent(
            tools,
            llm,
            agent="zero-shot-react-description",
            agent_kwargs={"prompt": prompt},
            verbose=True,
            handle_parsing_errors=True,
        )

        while True:
            query = input("\n❓ Ask about MCP or request code (or 'exit'): ")
            if query.lower() in {"exit", "quit"}:
                break
            response = await agent.ainvoke(query)
            print("\n💬", response)
            print("\n💬", response["output"])

if __name__ == "__main__":
    asyncio.run(main())