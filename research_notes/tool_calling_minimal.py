import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Functions
def get_weather(city: str) -> str:
    fake_weather = {
        "Paris": "18°C, cloudy",
        "Tokyo": "22°C, sunny",
        "Mumbai": "31°C, humid"
    }
    return fake_weather.get(city, f"No weather data for {city}")


def get_time(timezone: str) -> str:
    fake_time = {
        "Tokyo": "9:00 AM",
        "Paris": "2:00 AM",
        "Mumbai": "5:30 AM"
    }
    return fake_time.get(timezone, "Unknown")


# Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Gets current time for a city/timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "City name"}
                },
                "required": ["timezone"]
            }
        }
    }
]


# Registry
tool_registry = {
    "get_weather": get_weather,
    "get_time": get_time
}

def run_tool(name, args):
    return tool_registry[name](**args)


# The agent loop
messages = [
    {"role": "user", "content": "What's the weather in Mumbai and what's the time in Tokyo?"}
]

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    iteration += 1
    print(f"\n--- Iteration {iteration} ---")
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools
    )
    
    msg = response.choices[0].message
    stop_reason = response.choices[0].finish_reason
    
    messages.append({
        "role": "assistant",
        "content": msg.content or "",
        "tool_calls": msg.tool_calls
    })
    
    if stop_reason == "stop":
        print(f"\nFINAL ANSWER: {msg.content}")
        break
    
    if stop_reason == "tool_calls":
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = run_tool(name, args)
            print(f"TOOL: {name}({args}) → {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
else:
    print("Max iterations reached")