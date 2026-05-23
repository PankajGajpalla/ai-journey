import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

# response = llm.invoke("Say hello and tell me one fact about AI agents")
# print(response.content)

# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# messages = [
#     SystemMessage(content="You are a helpful AI tutor."),
#     HumanMessage(content="What is an AI agent?")
# ]

# response = llm.invoke(messages)
# print(response.content)


from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Gets the current weather for a city.
    
    Args:
        city: Name of the city like 'Paris' or 'Tokyo'
    """
    fake_weather = {
        "Paris": "18°C, cloudy",
        "Tokyo": "22°C, sunny",
        "Mumbai": "31°C, humid"
    }
    return fake_weather.get(city, f"No data for {city}")


print(get_weather.name)         # → get_weather
print(get_weather.description)  # → Gets the current weather...
print(get_weather.args)         # → {'city': {'title': 'City', 'type': 'string'}}