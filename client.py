import asyncio
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

from langchain_core.tools import tool                     
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model


DOC_PATH = Path(__file__).parent / "mcp_documentation.txt"
MCP_DOC  = DOC_PATH.read_text(encoding="utf-8").strip()

SYSTEM_PROMPT = """
You are an assistant expert in the MCP framework.
MCP is an open protocol that enables seamless integration between LLM applications and external data sources and tools.
Use the MCP documentation to answer any user questions about MCP's concepts, APIs or usage.
If the user asks you to generate code, ALWAYS delegate the request to the `generate_code` tool.
Only call one tool and return an answer to the user.
"""


@tool
async def get_doc(query: str) -> str:
    """Return the full MCP documentation."""
    print(query)
    return MCP_DOC

@tool
async def generate_code(query: str) -> str:
    """
    Route the request to a specialised coding agent that produces
    high-quality MCP framework code.
    """
    result = await mcp_client.call_tool("generate_mcp_code", {"query": query})
    return result[0].text

TOOLS = [get_doc, generate_code]


async def main() -> None:
    async with Client(PythonStdioTransport("server.py")) as client:
        global mcp_client
        mcp_client = client

        llm = init_chat_model("ollama:qwen3:1.7b", temperature=0.3)

        agent = create_react_agent(
            model=llm,
            tools=TOOLS,
            prompt=SYSTEM_PROMPT,
        )

        while True:
            query = input("\n❓  Ask about MCP or request code (type 'exit' to quit): ")
            if query.strip().lower() in {"exit", "quit"}:
                break


            async for node_update in agent.astream(
                    {"messages": [{"role": "user", "content": query}]},
                    stream_mode="updates"
            ):
                node, payload = next(iter(node_update.items()))
                for msg in payload["messages"]:
                    msg.pretty_print()

            print("─" * 40)
if __name__ == "__main__":
    asyncio.run(main())