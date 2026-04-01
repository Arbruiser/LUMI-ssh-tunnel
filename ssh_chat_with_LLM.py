import sys
import argparse
from openai import OpenAI

# 1. Connect to the local port forwarded by the SSH tunnel
client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key="token-ignored",
)

# 2. Parse the model name
parser = argparse.ArgumentParser()
parser.add_argument("MODEL", type=str, help="Name of the model as registered in vLLM")
args = parser.parse_args()

# 3. Initialize "messages" list which is the LLM's 'memory' of the conversation
messages = [
    {"role": "system", "content": "You are a helpful and concise AI assistant."}
]

print("--- Chat Started (Type 'quit' or 'exit' to stop) ---")

# 4. Start the chat
while True:
    # Get input from the user
    user_input = input("\nUser: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    # Add the user's message to the memory
    messages.append({"role": "user", "content": user_input})

    # Send a request to the LLM
    response = client.chat.completions.create(
        model=args.MODEL,
        messages=messages, 
        max_tokens=2000, 
        temperature=0.6, 
        stream=True 
    )

    print("LLM Response: ", end="", flush=True)
    response_text = "" 

    # Handle the stream and show the text
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            response_text += content

    # Add the LLM's response to the memory 
    messages.append({"role": "assistant", "content": response_text})
    print()