import openai
import json
import time
import argparse
import os
import subprocess
import requests


# openai.api_version = "2020-11-07"  # Set the correct API version here

# Directory to save output files
output_dir = "./responses"

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Function to generate response
def response(prompt, max_tokens, t, n, model="gpt-3.5-turbo"):
    try:
        # Convert JSON object to a string
        prompt_string = ''.join([f"{message['role']}: {message['content']}\n" for message in prompt])

        chunks = [prompt_string[i:i+max_tokens] for i in range(0, len(prompt_string), max_tokens)]
        responses = []
        for chunk in chunks:
            url = f"https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}"
            }
            data = {
                "model": model,
                "messages": [{"role": "system", "content": system_message}, {"role": "user", "content": user_prompt}],
                "n": n,
                "max_tokens": max_tokens,
                "stop": None,
                "temperature": t
            }
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                responses.append(response.json())
            else:
                print(f"An error occurred while generating text: {response.text}")
                return None
        return responses
    except Exception as e:
        print(f"An error occurred while generating text: {e}")
        return None

# Parsing input file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--system_message_file", help="Path to input file containing system message", default="./system-messages/_Default/189_youareanailangu_1679744083")
    parser.add_argument("input_file", help="Path to input file containing prompt text")
    parser.add_argument("--max_tokens", type=int, help="Maximum number of tokens per request", default=4000)
    parser.add_argument("--t", type=float, help="Temperature", default=0.4)
    parser.add_argument("--n", type=int, help="Number of responses", default=1)

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        user_prompt = f.read()

    # Read the system message from the specified file if provided
    if args.system_message_file:
        with open(args.system_message_file, "r") as f:
            system_message = f.read().strip()

    # Construct the messages input
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt},
    ]

    # Invoke function to get response
    generated_text = response(prompt=messages, max_tokens=args.max_tokens, t=args.t, n=args.n)
    if generated_text is not None:
        output_file = f"{output_dir}/output_{int(time.time())}.json"
        with open(output_file, "w") as f:
            f.write(json.dumps(generated_text))
        print(f"Wrote output to {output_file}")
    else:
        print("Failed to generate text.")
    time.sleep(1)  # Sleep for 1 second before requesting the next chunk

# Merge and extract the content
subprocess.run(["python", "./extract_merge_gpt3.5.py"])
