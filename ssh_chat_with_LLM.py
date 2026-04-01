import sys
import argparse
from openai import OpenAI

# 1. Ask the user for the generated API key
print("Please enter the API key found in your LUMI slurm output file.")
session_key = input("API Key: ").strip()

# 2. Connect to the local port forwarded by the SSH tunnel
client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key=session_key,
)

# 3. Parse the model name and the API key
parser = argparse.ArgumentParser()
parser.add_argument("MODEL", type=str, help="Name of the model as registered in vLLM")
parser.add_argument("API_KEY", type=str, help="API key from the SLURM output file")
args = parser.parse_args()

# 4. Initialize "messages" list which is the LLM's 'memory' of the conversation
messages = [
    {"role": "system", "content": "You are a helpful and concise AI assistant."}
]

print("--- Chat Started (Type 'quit' or 'exit' to stop) ---")

# 5. Start the chat
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