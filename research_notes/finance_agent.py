import os
import json
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class FinanceTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, note=""):
        
        # store amount, category, note, and a timestamp in a dict
        entry = {"amount":amount, "category": category, "note": note, "time_stamp": datetime.now().strftime("%Y-%m-%d")}

        # append it to self.expenses
        self.expenses.append(entry)

        # return a confirmation string
        return f"Logged ₹{amount} on {category}"
        

    def today_total(self):
        # sum amounts where the date is today
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(exp["amount"] for exp in self.expenses if exp["time_stamp"]==today)
    
    def weekly_total(self): 
        weekly = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d") 

        return sum(exp["amount"] for exp in self.expenses if exp["time_stamp"]>=weekly)

    def category_breakdown(self):
        exp_breakdown = {}

        for exp in self.expenses:
            exp_breakdown[exp["category"]]  = exp_breakdown.get(exp["category"], 0) + exp["amount"]
        
        return exp_breakdown

    def save(self, filename):
        with open(filename, "w") as file:
            json.dump(self.expenses, file, indent=4)
        
        return f"Saved {len(self.expenses)} expenses to {filename}"
    
    def load(self, filename):
        try:
            with open(filename, "r") as file:
                self.expenses = json.load(file)

            print(f"Loaded {len(self.expenses)} expenses")
        except FileNotFoundError:
            print(f"No saved data found at {filename}")
            self.expenses = []

tracker = FinanceTracker()

#wrapper
def add_expense_tool(amount, category, note=""):
    return tracker.add_expense(amount, category, note)

def today_total_tool():
    return f"Today's total: ₹{tracker.today_total()}"

def weekly_total_tool():
    return f"Weekly total: ₹{tracker.weekly_total()}"

def category_breakdown_tool():
    return f"Category breakdown: {tracker.category_breakdown()}"

def save_tool(filename):
    return tracker.save(filename)

def load_tool(filename):
    return tracker.load(filename)


#schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_expense_tool",
            "description": "adds users expense",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "amount value"},
                    "category": {"type": "string", "description": "type of expense"},
                    "note": {"type": "string", "description": "any note apart from amount and expense"}
                },
                "required": ["amount", "category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "today_total_tool",
            "description": "calculates the total expenditure for today",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weekly_total_tool",
            "description": "calculates the total expenditure for a week",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "category_breakdown_tool",
            "description": "calculates the expenditure for different categories",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_tool",
            "description": "save's the amount, category and note to the json file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "name of the file on which data is to be saved"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "load_tool",
            "description": "load and read the json file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "name of the file on which data is to be saved"}
                },
                "required": ["filename"]
            }
        }
    }
]

#Registry
tool_registry = {
    "add_expense_tool": add_expense_tool,
    "today_total_tool": today_total_tool,
    "weekly_total_tool": weekly_total_tool,
    "category_breakdown_tool": category_breakdown_tool,
    "save_tool": save_tool,
    "load_tool": load_tool
}

def run_tool(name, args):
    if name not in tool_registry:
        return f"Error: tool '{name}' not found"
    
    # remove any junk empty-key arguments the LLM might send
    clean_args = {k: v for k, v in args.items() if k}
    
    try:
        return tool_registry[name](**clean_args)
    except Exception as e:
        return f"Error running {name}: {e}"

print("Finance Assistant ready. Type 'quit' to exit.")
messages = [{"role": "system", "content": "You are a personal finance assistant that stores and calculate user's expense "}]


while True:                              # OUTER — conversation
    user_input = input("\nYou: ")
    if user_input == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    while True:                          # INNER — tool calling for THIS message
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        # build assistant message conditionally
        assistant_msg = {
            "role": "assistant",
            "content": msg.content or ""
        }
        if msg.tool_calls:
            assistant_msg["tool_calls"] = msg.tool_calls
        messages.append(assistant_msg)

        if stop_reason == "stop":
            print(f"\nAgent: {msg.content}")
            break

        if stop_reason == "tool_calls":
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = run_tool(name, args)
                print(f"  [tool: {name}({args}) → {result}]")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })