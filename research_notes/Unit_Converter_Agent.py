import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

# @tool
# def km_to_miles(km: float) -> float:
#     """Converts converts kilometers to miles (1 km = 0.621371 miles)
    
#     Args:
#         km: value in kilometers
#     """
#     return f"{km*0.621371} miles"

# @tool
# def kg_to_pounds(kg: float) -> float:
#     """converts kilograms to pounds (1 kg = 2.20462 pounds)

#     Args:
#         kg: value in kilogram
#     """

#     return f"{kg*2.20462} pounds"

# @tool
# def celsius_to_fahrenheit(celsius: float) -> float:
#     """converts value in celsius to fahrenheit.

#     Args:
#         celsius: value in celsius
#     """
#     return f"{(celsius*9/5) + 32}°F"

# tools = [km_to_miles, kg_to_pounds, celsius_to_fahrenheit]
# llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
# agent = create_agent(llm, tools)

# result = agent.invoke({
#     "messages": [("user", "Convert 100 km to miles, 75 kg to pounds, and 30°C to Fahrenheit")]
# })

# print(result["messages"][-1].content)

@tool
def count_words(text: str) -> str:
    """returns the word count.

    Args:
        text: any text
    """
    return f"Word Count: {len(text.split(' '))}"


@tool
def count_characters(text: str) -> str:
    """returns character count.

    Args:
        text: any text
    """

    return f"Character count{sum(1 for t in text if t!=' ')}"

@tool
def to_uppercase(text: str) -> str:
    """returns text in uppercase.

    Args:
        text: any text
    """
    return text.upper()

@tool
def find_longest_word(text: str) -> str:
    """returns the longest word.

    Args:
        text: any text
    """
    longest = ""
    for t in text.strip().split():
        if len(longest)<len(t):
            longest = t
    
    return longest


tools = [count_words, count_characters, to_uppercase, find_longest_word]
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
agent = create_agent(llm, tools)

result = agent.invoke({
    "messages": [("user", "For the text 'artificial intelligence is transforming the world', count the words, find the longest word, and convert it to uppercase")]
})

print(result["messages"][-1].content)


# @tool
# def get_population(country: str) -> str:
#     """returns fake population data for countries
#     Args:
#         country: name of the country like 'India'
#     """
#     countries = {"India": 1000, "USA": 500, "China": 1299, "Japan": 394}
#     return countries.get(country, f"data not available")

# @tool
# def get_capital(country: str) -> str:
#     """returns the capital city.

#     Args:
#         country: name of a country like 'India'
#     """

#     countries = {"India": "Delhi", "USA": "Washington DC", "China": "Bejing", "Japan": "Tokyo"}
#     return countries.get(country, f"data not available")

# @tool
# def calculator(expression: str) -> str:
#     """evaluates a  math expression.

#     Args:
#         expression: A math expression like '2 * 5'
#     """
#     try:
#         return str(eval(expression))
#     except Exception as e:
#         return f"Error: {e}"
    
# tools = [get_population, get_capital, calculator]
# llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
# agent = create_agent(llm, tools)

# result = agent.invoke({
#     "messages": [("user", "What's the capital of India, and if India has the population you know, what would 10% of it be?")]
# })

# for message in result["messages"]:
#     message.pretty_print()




# output
# 1.
# The capital of India is **Delhi**.  
# With the population figure you provided (1,000 people), 10 % of that would be **100 people**.

# 2.
# **Word Count:** 6  
# **Longest Word:** *intelligence*  
# **Longest Word in Uppercase:** **INTELLIGENCE**

# 3.
# ================================ Human Message =================================

# What's the capital of India, and if India has the population you know, what would 10% of it be?
# ================================== Ai Message ==================================
# Tool Calls:
#   get_capital (fc_df5a00c5-47d9-4127-8aec-f879b7228844)
#  Call ID: fc_df5a00c5-47d9-4127-8aec-f879b7228844
#   Args:
#     country: India
# ================================= Tool Message =================================
# Name: get_capital

# Delhi
# ================================== Ai Message ==================================
# Tool Calls:
#   get_population (fc_fad04cb7-8cc3-40b9-a0d3-1b41e4c27cfc)
#  Call ID: fc_fad04cb7-8cc3-40b9-a0d3-1b41e4c27cfc
#   Args:
#     country: India
# ================================= Tool Message =================================
# Name: get_population

# 1000
# ================================== Ai Message ==================================

# The capital of India is **New Delhi**.  
# According to the population data you provided, India has **1,000** people.  
# \[
# \frac{10}{100} \times 1{,}000 = 100
# \]

# So 10 % of India's population would be **100** people.