import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Gets weather for a city.

    Args:
        city: Name of the city
    """
    weather = {"Tokyo": "22°C, sunny", "Mumbai": "31°C, humid"}
    return weather.get(city, "No data")


tools = [get_weather]
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
agent = create_agent(llm, tools)

# Stream the agent's steps
for chunk in agent.stream(
    {"messages": [("user", "What's the weather in Tokyo? Then tell me a fun fact about it.")]},
    stream_mode="values"
):
    # each chunk is the current state — print the latest message
    latest = chunk["messages"][-1]
    latest.pretty_print()