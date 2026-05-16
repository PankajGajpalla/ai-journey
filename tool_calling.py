# How tool calling works

# Step 1 — define your tools
import json
import os
import math
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Tool 1 — calculator
def calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Tool 2 — word counter
def word_counter(text: str) -> str:
    words = len(text.split())
    chars = len(text)
    return f"Words: {words}, Characters: {chars}"


# Tool 3 — text reverser
def reverse_text(text: str) -> str:
    return text[::-1]


# Tool 4 — unit converter
def celsius_to_fahrenheit(celsius: float) -> str:
    f = (celsius * 9/5) + 32
    return f"{celsius}°C = {f}°F"


# Tool 5 - get_current_time()
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

# Tool 6 - list_analyzer
def list_analyzer(numbers: str) -> str:
    li = [int(n.strip()) for n in numbers.split(",")]
    total = sum(li)
    avg = total / len(li)
    return f"Count: {len(li)}\nSum: {total}\nAverage: {avg}\nMax: {max(li)}\nMin: {min(li)}"

# Tool 7 text_analyzer(text: str)
def text_analyzer(text: str) -> str:
    words = text.split()
    unique_words = set(words)
    longest = max(words, key=len)
    uppercase_count = sum(1 for c in text if c.isupper())
    
    return (
        f"Words: {len(words)}\n"
        f"Unique words: {len(unique_words)}\n"
        f"Longest word: {longest}\n"
        f"Uppercase: {uppercase_count}"
    )

 


# Step 2 — describe tools to the LLM
# The LLM needs to know what tools exist and what they do. You describe them in a specific format:

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a mathematical expression and returns the result. Use for any math calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '347 * 892' or '100 / 4 + 5'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "word_counter",
            "description": "Counts words and characters in a given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count words in"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reverse_text",
            "description": "Reverses the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "celsius_to_fahrenheit",
            "description": "Converts temperature from Celsius to Fahrenheit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "celsius": {
                        "type": "number",
                        "description": "Temperature in Celsius"
                    }
                },
                "required": ["celsius"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "tells the current time to the user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_analyzer",
            "description": "Converts string comma seprated numbers to a list of numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "string",
                        "description": "list in string formate e.g '5,10,15,20'"
                    }
                },
                "required": ["numbers"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "text_analyzer",
            "description": "analyzes a text and tell its words, unique words, longest word, and uppercase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "analyzes of text"
                    }
                },
                "required": ["text"]
            }
        }
    }
]


# Step 3 — a registry to call tools by name
tool_registry = {
    "calculator": calculator,
    "word_counter": word_counter,
    "reverse_text": reverse_text,
    "celsius_to_fahrenheit": celsius_to_fahrenheit,
    "get_current_time": get_current_time,
    "list_analyzer": list_analyzer,
    "text_analyzer": text_analyzer
}

def run_tool(name: str, arguments: dict) -> str:
    if name in tool_registry:
        return tool_registry[name](**arguments)
    return f"Error: Tool '{name}' not found"


# Step 4 — the agent loop

def run_agent(user_message: str):
    print(f"\nUser: {user_message}")
    print("─" * 40)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. Use tools when needed to answer accurately. Think step by step."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # agent loop — keeps going until LLM gives a final answer
    while True:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        except Exception as e:
            print(f"⚠ API error: {e}")
            break

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        # add assistant message to history
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": message.tool_calls if message.tool_calls else None
        })

        # if LLM is done — no more tool calls needed
        if stop_reason == "stop":
            print(f"\nAgent: {message.content}")
            break

        # if LLM wants to call tools
        if stop_reason == "tool_calls" and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"→ Calling tool: {tool_name}({tool_args})")

                result = run_tool(tool_name, tool_args)

                print(f"← Tool result: {result}")

                # send tool result back to LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

# step 5 -- run it
# run_agent("What is 347 multiplied by 892?")
# run_agent("How many words are in 'The quick brown fox jumps over the lazy dog'?")
# run_agent("Convert 37 degrees Celsius to Fahrenheit")
# run_agent("What is 15% of 8500, and then reverse the word 'intelligence'?")
run_agent("What time is it right now?")
run_agent("Analyze these numbers: 12, 45, 7, 89, 23, 56")
run_agent("Analyze this text: The quick brown fox jumps over the lazy dog")
run_agent("What time is it, and what is the average of 10, 20, 30, 40, 50?")

























# # How tool calling works

# # Step 1 — define your tools
# import json
# import os
# import math
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# # Tool 1 — calculator
# def calculator(expression: str) -> str:
#     try:
#         result = eval(expression)
#         return str(result)
#     except Exception as e:
#         return f"Error: {e}"


# # Tool 2 — word counter
# def word_counter(text: str) -> str:
#     words = len(text.split())
#     chars = len(text)
#     return f"Words: {words}, Characters: {chars}"


# # Tool 3 — text reverser
# def reverse_text(text: str) -> str:
#     return text[::-1]


# # Tool 4 — unit converter
# def celsius_to_fahrenheit(celsius: float) -> str:
#     f = (celsius * 9/5) + 32
#     return f"{celsius}°C = {f}°F"



# # Step 2 — describe tools to the LLM
# # The LLM needs to know what tools exist and what they do. You describe them in a specific format:

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "calculator",
#             "description": "Evaluates a mathematical expression and returns the result. Use for any math calculation.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "expression": {
#                         "type": "string",
#                         "description": "The math expression to evaluate, e.g. '347 * 892' or '100 / 4 + 5'"
#                     }
#                 },
#                 "required": ["expression"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "word_counter",
#             "description": "Counts words and characters in a given text.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "text": {
#                         "type": "string",
#                         "description": "The text to count words in"
#                     }
#                 },
#                 "required": ["text"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "reverse_text",
#             "description": "Reverses the given text.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "text": {
#                         "type": "string",
#                         "description": "The text to reverse"
#                     }
#                 },
#                 "required": ["text"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "celsius_to_fahrenheit",
#             "description": "Converts temperature from Celsius to Fahrenheit.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "celsius": {
#                         "type": "number",
#                         "description": "Temperature in Celsius"
#                     }
#                 },
#                 "required": ["celsius"]
#             }
#         }
#     }
# ]


# # Step 3 — a registry to call tools by name
# tool_registry = {
#     "calculator": calculator,
#     "word_counter": word_counter,
#     "reverse_text": reverse_text,
#     "celsius_to_fahrenheit": celsius_to_fahrenheit
# }

# def run_tool(name: str, arguments: dict) -> str:
#     if name in tool_registry:
#         return tool_registry[name](**arguments)
#     return f"Error: Tool '{name}' not found"


# # Step 4 — the agent loop

# def run_agent(user_message: str):
#     print(f"\nUser: {user_message}")
#     print("─" * 40)

#     messages = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant with access to tools. Use tools when needed to answer accurately. Think step by step."
#         },
#         {
#             "role": "user",
#             "content": user_message
#         }
#     ]

#     # agent loop — keeps going until LLM gives a final answer
#     while True:
#         try:
#             response = client.chat.completions.create(
#                 model="openai/gpt-oss-20b",
#                 messages=messages,
#                 tools=tools,
#                 tool_choice="auto"
#             )
#         except Exception as e:
#             print(f"⚠ API error: {e}")
#             break

#         message = response.choices[0].message
#         stop_reason = response.choices[0].finish_reason

#         # add assistant message to history
#         messages.append({
#             "role": "assistant",
#             "content": message.content or "",
#             "tool_calls": message.tool_calls if message.tool_calls else None
#         })

#         # if LLM is done — no more tool calls needed
#         if stop_reason == "stop":
#             print(f"\nAgent: {message.content}")
#             break

#         # if LLM wants to call tools
#         if stop_reason == "tool_calls" and message.tool_calls:
#             for tool_call in message.tool_calls:
#                 tool_name = tool_call.function.name
#                 tool_args = json.loads(tool_call.function.arguments)

#                 print(f"→ Calling tool: {tool_name}({tool_args})")

#                 result = run_tool(tool_name, tool_args)

#                 print(f"← Tool result: {result}")

#                 # send tool result back to LLM
#                 messages.append({
#                     "role": "tool",
#                     "tool_call_id": tool_call.id,
#                     "content": result
#                 })

# # step 5 -- run it
# run_agent("What is 347 multiplied by 892?")
# run_agent("How many words are in 'The quick brown fox jumps over the lazy dog'?")
# run_agent("Convert 37 degrees Celsius to Fahrenheit")
# run_agent("What is 15% of 8500, and then reverse the word 'intelligence'?")
# run_agent("What time is it right now?")
# run_agent("Analyze these numbers: 12, 45, 7, 89, 23, 56")
# run_agent("Analyze this text: The quick brown fox jumps over the lazy dog")
# run_agent("What time is it, and what is the average of 10, 20, 30, 40, 50?")