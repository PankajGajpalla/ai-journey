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
    
    # Append assistant message
    messages.append({
        "role": "assistant",
        "content": msg.content or "",
        "tool_calls": msg.tool_calls
    })
    
    # If LLM is done, exit
    if stop_reason == "stop":
        print(f"\nFINAL ANSWER: {msg.content}")
        break
    
    # If LLM wants tools, run them all
    if stop_reason == "tool_calls":
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = run_tool(name, args)
            print(f"TOOL: {name}({args}) → {result}")
            
 