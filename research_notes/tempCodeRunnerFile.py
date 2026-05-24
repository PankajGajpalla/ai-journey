
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