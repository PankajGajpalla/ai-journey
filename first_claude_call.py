import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

personas = {
    "1": {
        "name": "Python Expert",
        "system": "You are an expert Python tutor. Explain concepts simply with short code examples."
    },
    "2": {
        "name": "AI Agent Specialist",
        "system": "You are an AI agent specialist. Explain agent concepts practically and concisely."
    },
    "3": {
        "name": "Career Coach",
        "system": "You are a tech career coach helping someone become an AI engineer. Be motivating and practical."
    }
}

prompt_tokens = 0
completion_tokens = 0
total_tokens = 0
conversation_history = []


def show_menu():
    print("\nChoose your AI tutor:")
    for key, persona in personas.items():
        print(f"  {key}. {persona['name']}")
    print()


def get_choice():
    while True:
        choice = input("Enter choice (1/2/3): ").strip()
        if choice in personas:
            return choice
        print("Invalid choice. Enter 1, 2, or 3.")


def setup_persona(choice):
    conversation_history.clear()
    conversation_history.append({
        "role": "system",
        "content": personas[choice]["system"]
    })
    print(f"\n✓ {personas[choice]['name']} is ready. Type your message, or 'quit', 'history', 'reset'.\n")


def chat(user_message):
    global prompt_tokens, completion_tokens, total_tokens

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history,
        stream=True
    )

    print("AI: ", end="", flush=True)
    assistant_message = ""

    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text:
            print(text, end="", flush=True)
            assistant_message += text

    print("\n")

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    # non-streaming call to get token count
    usage_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_message}]
    )
    prompt_tokens += usage_response.usage.prompt_tokens
    completion_tokens += usage_response.usage.completion_tokens
    total_tokens += usage_response.usage.total_tokens


def show_history():
    print("\n--- Conversation History ---")
    for i, msg in enumerate(conversation_history):
        if msg["role"] == "system":
            continue
        print(f"{i}. [{msg['role'].upper()}] {msg['content'][:100]}")
    print()


def show_summary():
    messages = len([m for m in conversation_history if m["role"] != "system"])
    print("\nSession Summary")
    print("─" * 30)
    print(f"Messages exchanged: {messages}")
    print(f"Prompt tokens:      {prompt_tokens}")
    print(f"Completion tokens:  {completion_tokens}")
    print(f"Total tokens:       {total_tokens}")
    print("Cost: Free on Groq 😄")


# startup
show_menu()
choice = get_choice()
setup_persona(choice)

# main loop
while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    elif user_input.lower() == "quit":
        show_summary()
        break
    elif user_input.lower() == "history":
        show_history()
    elif user_input.lower() == "reset":
        show_menu()
        choice = get_choice()
        setup_persona(choice)
        prompt_tokens = completion_tokens = total_tokens = 0
    else:
        chat(user_input)






















































# chatbot.py

# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# personas = {
#     "1": {
#         "name": "Python Expert",
#         "system": "You are an expert Python tutor. Explain concepts simply with short code examples."
#     },
#     "2": {
#         "name": "AI Agent Specialist",
#         "system": "You are an AI agent specialist. Explain agent concepts practically and concisely."
#     },
#     "3": {
#         "name": "Career Coach",
#         "system": "You are a tech career coach helping someone become an AI engineer. Be motivating and practical."
#     }
# }

# # YOUR CODE BELOW
# # 1. Show menu, get persona choice
# # 2. Set up conversation_history with system prompt
# # 3. Chat loop with input()
# # 4. Handle: quit, history, reset, normal message
# # 5. Track total_tokens across all calls
# # 6. On quit print summary
# def choice():
#     c = input("chose from menu 1,2,3 persona: ")
#     return c

# def show_menu():
#     print("chose persona")
#     for e,i in enumerate(personas):
#         print(f"{e+1}. {personas[i]["name"]}")
    
#     print("*"*10)

# show_menu()

# choice = choice()

# conversation_history = [
#         {
#             "role": "system",
#             "content": personas[choice]["system"]
#         }
#     ]



# prompt_tokens, completion_tokens, total_tokens = 0,0,0


# def chat(user_message):
#     conversation_history.append(
#         {
#             "role": "user",
#             "content": user_message
#         }
#     )

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages= conversation_history
#     )

#     assistant_message = response.choices[0].message.content

#     conversation_history.append({
#         "role": "assistant",
#         "content": assistant_message
#     })

#     prompt_tokens = response.usage.prompt_tokens
#     completion_tokens = response.usage.completion_tokens
#     total_tokens = response.usage.total_tokens

#     return assistant_message

# def summary():
#     print("summary")
#     print(f"\nTokens — Prompt: {prompt_tokens} | Completion: {completion_tokens} | Total: {total_tokens}")
#     print("Cost: Free on Groq 😄")


# def show_history():
#     for j in conversation_history:
#         print(f"role: {j['role']}")
#         print(f"content: {j['content']}")
#         print()



# options = {1:"quit", 2:"history", 3:"reset", 4:"normal message"}

# select = "normal message"

# while(select!="quit"):
#     print("chose_operations: 1, 2, 3, 4")
#     select = options[int(input(f"{options} : "))]

#     if select == "quit":
#         summary()
#         break
#     elif select == "history":
#         show_history()
#     elif select == "reset":
#         conversation_history = []
#         print("reset done")
        
#         show_menu()
#         choice = choice()
#         conversation_history = [
#                 {
#                     "role": "system",
#                     "content": personas[choice]["system"]
#                 }
#             ]

#     else:
#         user_message = input("enter your message: ")
#         print(chat(user_message))
        














































# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def chat_with_cost(message_text):
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": message_text}]
#     )

#     prompt_tokens = response.usage.prompt_tokens
#     completion_tokens = response.usage.completion_tokens
#     total_tokens = response.usage.total_tokens

#     print(f"Response: {response.choices[0].message.content}")
#     print(f"\nTokens — Prompt: {prompt_tokens} | Completion: {completion_tokens} | Total: {total_tokens}")
#     print("Cost: Free on Groq 😄")


# chat_with_cost("What is the capital of France?")

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are an expert Python tutor who teaches beginners. Always explain concepts simply with short code examples. Never use jargon without explaining it first."
#         },
#         {
#             "role": "user",
#             "content": "What is a decorator?"
#         }
#     ]
# )

# print(response.choices[0].message.content)
# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def analyze_topic(topic):
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a curriculum designer.
#                 Always respond with valid JSON only. No extra text, no markdown, no backticks.
#                 JSON format:
#                 {
#                     "topic": "string",
#                     "difficulty": "beginner/intermediate/advanced",
#                     "prerequisites": ["list", "of", "prerequisites"],
#                     "key_concepts": ["list", "of", "concepts"],
#                     "estimated_hours": number
#                 }"""
#             },
#             {
#                 "role": "user",
#                 "content": f"Analyze this learning topic: {topic}"
#             }
#         ]
#     )

#     raw = response.choices[0].message.content
#     return json.loads(raw)


# result = analyze_topic("LangChain agents")
# print(f"Topic: {result['topic']}")
# print(f"Difficulty: {result['difficulty']}")
# print(f"Hours needed: {result['estimated_hours']}")
# print(f"Prerequisites: {', '.join(result['prerequisites'])}")
# print(f"Key concepts: {', '.join(result['key_concepts'])}")

# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# stream = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {"role": "user", "content": "Explain what RAG is in 3 sentences"}
#     ],
#     stream=True
# )

# for chunk in stream:
#     text = chunk.choices[0].delta.content
#     if text:
#         print(text, end="", flush=True)

# print()



# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# conversation_history = [
#     {
#         "role": "system",
#         "content": "You are a helpful AI engineering tutor."
#     }
# ]

# def chat(user_message):
#     conversation_history.append({
#         "role": "user",
#         "content": user_message
#     })

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=conversation_history
#     )

#     assistant_message = response.choices[0].message.content

#     conversation_history.append({
#         "role": "assistant",
#         "content": assistant_message
#     })

#     return assistant_message


# print(chat("What is an AI agent?"))
# print("---")
# print(chat("What tools can it use?"))
# print("---")
# print(chat("Give me a simple Python example"))





# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {"role": "user", "content": "Say hello and tell me one interesting fact about AI agents"}
#     ]
# )

# print(response.choices[0].message.content)  # the text
# print(response.model)                        # which model responded
# print(response.usage.prompt_tokens)          # tokens you sent
# print(response.usage.completion_tokens)      # tokens AI generated
# print(response.usage.total_tokens)           # total tokens used



# import os
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# response = client.models.generate_content(
#     model="gemini-1.5-flash",
#     contents="Say hello and tell me one interesting fact about AI agents"
# )

# print(response.text)

# import anthropic
# from dotenv import load_dotenv

# load_dotenv()

# client = anthropic.Anthropic()

# message = client.messages.create(
#     model="claude-sonnet-4-6",
#     max_tokens=1024,
#     messages=[
#         {"role":"user", "content":"Say hello and tell me one interesting fact about AI agents"}
#     ]

# )

# print(message.content[0].text)