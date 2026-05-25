import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Gets the current weather for a city.

    Args:
        city: Name of the city
    """
    weather = {"Paris": "18°C, cloudy", "Tokyo": "22°C, sunny", "Mumbai": "31°C, humid"}
    return weather.get(city, f"No data for {city}")


tools = [get_weather]
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

# Add the checkpointer for memory
checkpointer = MemorySaver()
agent = create_agent(llm, tools, checkpointer=checkpointer)

# Same thread_id = same conversation
config = {"configurable": {"thread_id": "chat_1"}}

# Turn 1
result = agent.invoke(
    {"messages": [("user", "My name is Luffy and I live in Mumbai")]},
    config
)
print("Turn 1:", result["messages"][-1].content)

# Turn 2 — references info from turn 1
result = agent.invoke(
    {"messages": [("user", "What's my name and what's the weather where I live?")]},
    config
)
print("Turn 2:", result["messages"][-1].content)

# Different thread_id = fresh conversation, no memory of Luffy
new_config = {"configurable": {"thread_id": "chat_2"}}

result = agent.invoke(
    {"messages": [("user", "What's my name?")]},
    new_config
)
print("Different thread:", result["messages"][-1].content)
# Agent won't know — different conversation
