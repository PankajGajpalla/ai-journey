import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """ returns weather of a city
    
    Args:
        city: Name of the city
    """
    fake_weather = weather = {"Paris": "18°C, cloudy", "Tokyo": "22°C, sunny", "Mumbai": "31°C, humid"}
    return weather.get(city, f"No data for {city}")

@tool
def calculator(expression: str) -> str:
    """ Evaluates a math expression
    
    Args:
        expression: A math expression like '2 * 3' """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"error: {e}"

tools = [get_weather, calculator]
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

checkpointer = MemorySaver()
agent = create_agent(llm, tools, checkpointer=checkpointer)

config = {"configurable": {"thread_id": "chat_1"}}

print("Chat ready. Type 'quit' to exit.")

while True:
    user_input = input("\nYou: ")
    if user_input == "quit":
        break
    
    result = agent.invoke(
        {"messages": [("user", user_input)]},
        config
    )
    print("Agent:", result["messages"][-1].content)

