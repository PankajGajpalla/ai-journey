import os
import json
import requests
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS
from bs4 import BeautifulSoup

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Step 3 — build Tool 1: web search

def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo. Returns top results as text."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"No results found for '{query}'"
        
        output = f"Search results for '{query}':\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. {r['title']}\n"
            output += f"   URL: {r['href']}\n"
            output += f"   Summary: {r['body']}\n\n"
        
        return output
    except Exception as e:
        return f"Search error: {e}"

print(search_web("LangChain framework", max_results=3))

print("*"*20)

# Step 4 — build Tool 2: fetch and read a URL
def fetch_url(url: str) -> str:
    """Fetches a webpage and extracts clean text content. Returns up to 3000 characters."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (research-agent)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # remove scripts, styles, navigation
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        
        # truncate to avoid huge token usage
        if len(text) > 3000:
            text = text[:3000] + "...[truncated]"
        
        return f"Content from {url}:\n\n{text}"
    except Exception as e:
        return f"Fetch error: {e}"

print(fetch_url("https://en.wikipedia.org/wiki/Large_language_model"))
print("*"*20)

# Step 5 — build Tool 3: save a note
def save_note(filename: str, content: str) -> str:
    """Saves research notes to a markdown file."""
    try:
        os.makedirs("research_notes", exist_ok=True)
        
        if not filename.endswith(".md"):
            filename += ".md"
        
        filepath = os.path.join("research_notes", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Research Note\n\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(content)
        
        return f"Successfully saved to {filepath}"
    except Exception as e:
        return f"Save error: {e}"
    

print(save_note("test_note", "This is a test note about AI agents."))
print("*"*20)

# Step 6 — wire all 3 tools to the agent

# Tool descriptions for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the web using DuckDuckGo. Use this to find information on any topic. Returns top results with titles, URLs, and summaries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g. 'top AI agent frameworks 2026'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results to return, default 5"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Fetches a webpage and extracts the main text content. Use this AFTER search_web to read the full content of a specific result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full URL to fetch, e.g. 'https://example.com/article'"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Saves research notes to a markdown file in the research_notes folder. Use this at the end to persist findings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename without extension, e.g. 'ai_agents_comparison'"
                    },
                    "content": {
                        "type": "string",
                        "description": "The markdown content to save"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    }
]


# Registry
tool_registry = {
    "search_web": search_web,
    "fetch_url": fetch_url,
    "save_note": save_note
}


def run_tool(name: str, arguments: dict) -> str:
    if name in tool_registry:
        return tool_registry[name](**arguments)
    return f"Error: Tool '{name}' not found"


# Step 7 — the agent loop

def run_research_agent(user_message: str, max_iterations: int = 10):
    print(f"\n{'='*60}")
    print(f"🔍 Task: {user_message}")
    print(f"{'='*60}\n")

    messages = [
        {
            "role": "system",
            "content": """You are a research assistant agent. You can search the web, read pages, and save notes.

Workflow:
1. Use search_web to find relevant sources
2. Use fetch_url to read 2-3 of the most promising results in detail
3. Synthesize findings into clear, useful notes
4. Use save_note to persist your final research

Be thorough but efficient. Don't fetch every result — pick the best 2-3."""
        },
        {"role": "user", "content": user_message}
    ]

    for iteration in range(max_iterations):
        print(f"\n--- Step {iteration + 1} ---")

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

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": message.tool_calls if message.tool_calls else None
        })

        if stop_reason == "stop":
            print(f"\n{'='*60}")
            print(f"✅ Final Answer:\n")
            print(message.content)
            print(f"{'='*60}\n")
            return message.content

        if stop_reason == "tool_calls" and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"🛠  Tool: {tool_name}")
                print(f"   Args: {tool_args}")

                result = run_tool(tool_name, tool_args)

                # truncate display only — full result still goes to LLM
                display = result[:300] + "..." if len(result) > 300 else result
                print(f"📥 Result: {display}\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

    print("⚠ Max iterations reached")
    return None


# Step 8 — run real research tasks
run_research_agent("Research the top 3 AI agent frameworks (LangChain, CrewAI, AutoGen). Save a comparison note covering: what each is, key strengths, and best use cases.")

# Task 1 — the framework comparison above

# Task 2 — current news
run_research_agent("What are the latest developments in AI agents in 2026? Save a brief summary.")

# Task 3 — technical research
run_research_agent("Research what RAG (Retrieval Augmented Generation) is, how it works, and save key concepts.")