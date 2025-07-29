import asyncio
import os
import signal

from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_ollama import ChatOllama

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

SERVER_URL = os.getenv("MCP_SERVER_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

SYSTEM_PROMPT = """\
You are a friendly and helpful assistant with limited capabilities. You are part of chat bot application.
You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.
You should always stick to a natural conversational flow, while answering extensively.

## Tools

You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask. Use your tools to provide the best possible answer.

## Output Format

Always answer in the same language as the question.
Never surround your response with markdown code markers. You may use code markers within your response if you need to.

## Groundedness

Base your responses in facts whenever possible. Use anything that may help you prevent hallucination (like tools, docs, chat history).
"""


async def main() -> None:

    async with sse_client(url=SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            tools = await load_mcp_tools(session)
            llm = ChatOllama(
                model=MODEL_NAME, base_url="http://ollama:11434", temperature=0.3
            )

            # Set debug to True if you want to see all different steps the agent takes to solve the task
            graph = create_react_agent(
                model=llm,
                tools=tools,
                prompt=SYSTEM_PROMPT,
                checkpointer=memory,
            )
            while True:
                query = input(
                    "\n❓  Ask about MCP or request code (type 'exit' to quit): "
                )
                if len(query.strip()) == 0:
                    continue

                if query.strip().lower() in ["exit"]:
                    break
                async for node_update in graph.astream(
                    {"messages": [{"role": "user", "content": query}]},
                    stream_mode="updates",
                    config={"configurable": {"thread_id": "thread-1"}},
                ):
                    node, payload = next(iter(node_update.items()))
                    for msg in payload["messages"]:
                        msg.pretty_print()

                print("─" * 40)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    asyncio.run(main())
