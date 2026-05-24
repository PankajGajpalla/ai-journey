import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
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


@tool
def calculator(expression: str) -> str:
    """Evaluates a math expression.

    Args:
        expression: A math expression like '5 * 10'
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


tools = [get_weather, calculator]
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
agent = create_agent(llm, tools)

# stream the steps to see the agent thinking
result = agent.invoke({
    "messages": [("user", "What's the weather in Mumbai and what's 88 * 12?")]
})

# print every message in the conversation
for message in result["messages"]:
    message.pretty_print()

















# import os
# from langchain_groq import ChatGroq
# from langchain_core.tools import tool
# from langchain.agents import create_agent
# from dotenv import load_dotenv

# load_dotenv()


# @tool
# def get_weather(city: str) -> str:
#     """Gets the current weather for a city.

#     Args:
#         city: Name of the city
#     """
#     weather = {"Paris": "18°C, cloudy", "Tokyo": "22°C, sunny", "Mumbai": "31°C, humid"}
#     return weather.get(city, f"No data for {city}")


# @tool
# def calculator(expression: str) -> str:
#     """Evaluates a math expression.

#     Args:
#         expression: A math expression like '5 * 10'
#     """
#     try:
#         return str(eval(expression))
#     except Exception as e:
#         return f"Error: {e}"


# tools = [get_weather, calculator]
# llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

# # create_react_agent builds the whole agent in ONE line
# agent = create_agent(llm, tools)

# # Run it
# result = agent.invoke({
#     "messages": [("user", "What's the weather in Tokyo and what's 234 * 56?")]
# })

# # Print the final message
# print(result["messages"][-1].content)