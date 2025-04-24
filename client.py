import asyncio
from langchain_community.llms import Ollama
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from langchain.tools import tool
from langchain.agents import initialize_agent


async def main():
    async with Client(PythonStdioTransport("weather.py")) as client:
        llm = Ollama(model="mistral")

        @tool
        async def get_forecast(city: str) -> str:
            """Get a 5-day weather forecast for a city like 'Paris' or 'Berlin'."""
            try:
                cleaned = city.replace('"', '').replace("'", "").strip()
                result = await client.call_tool("get_forecast", {"city": cleaned})
                return result[0].text.strip()
            except Exception as e:
                return f"Error fetching forecast: {e}"

        tools = [get_forecast]

        agent = initialize_agent(
            tools,
            llm,
            agent="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True,
        )

        while True:
            query = input("\n❓ Ask the weather agent something (or type 'exit'): ")
            if query.lower() in {"exit", "quit"}:
                break

            response = await agent.ainvoke(query)
            print("\n🛰️ Forecast:\n", response)


if __name__ == "__main__":
    asyncio.run(main())