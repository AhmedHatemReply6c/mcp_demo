import asyncio
import os

from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_ollama import ChatOllama

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools


SERVER_URL = os.getenv("MCP_SERVER_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

SYSTEM_PROMPT = """\
You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Tools

You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask.

You have access to the following tools:
{tools}


## Output Format

Please answer in the same language as the question and use the following format:

```
<think>
The current language of the user is: (user's language). I need to use a tool to help me answer the question.
</think>
Action: tool name (one of {tool_names}) if using a tool.
Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
```

Please ALWAYS start with a Thought in the <thinking> tags.

NEVER surround your response with markdown code markers. You may use code markers within your response if you need to.

Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

If this format is used, the tool will respond in the following format:

```
Observation: tool response
```

You should keep repeating the above format till you have enough information to answer the question without using any more tools. At that point, you MUST respond in one of the following two formats:

```
<think>
I can answer without using any more tools. I'll use the user's language to answer.
</think>
[your answer here (In the same language as the user's question)]
```

```
<think>
I cannot answer the question with the provided tools.
</think>
[your answer here (In the same language as the user's question)]
```

## Current Conversation

Below is the current conversation consisting of interleaving human and assistant messages.

Question: {input}
Thought:{agent_scratchpad}
"""


async def main() -> None:
    async with sse_client(url=SERVER_URL) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(tools)
            llm = ChatOllama(model=MODEL_NAME, base_url="http://ollama:11434", temperature=0.3)

            graph = create_react_agent(
                model=llm, tools=tools, prompt=SYSTEM_PROMPT, debug=True
            )

            while True:
                query = input(
                    "\n❓  Ask about MCP or request code (type 'exit' to quit): "
                )
                if query.strip().lower() in ["exit"]:
                    break

                async for node_update in graph.astream(
                    {"messages": [{"role": "user", "content": query}]},
                    stream_mode="updates",
                    debug=True,
                ):
                    node, payload = next(iter(node_update.items()))
                    for msg in payload["messages"]:
                        msg.pretty_print()

                print("─" * 40)


if __name__ == "__main__":
    asyncio.run(main())
