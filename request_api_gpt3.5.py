import openai
import json
import time
import argparse
import os
import subprocess
import requests
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class InvalidRequestError(Exception):
    pass
class InvalidJSONError(Exception):
    pass

output_dir = "./responses"
os.makedirs(output_dir, exist_ok=True)
extracts_dir = "./extracts"
os.makedirs(extracts_dir, exist_ok=True)

@retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(10), retry=retry_if_exception_type(InvalidRequestError))
def response(prompt, max_tokens, t, n, system_message, user_prompt, top_p, frequency_penalty, presence_penalty, assistant_message=None, model="gpt-3.5-turbo"):
    try:
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_prompt}]
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})

        url = f"https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "n": n,
            "max_tokens": max_tokens,
            "stop": None,
            "temperature": t,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            try:
                response_json = response.json()
                return response_json
            except json.JSONDecodeError:
                raise InvalidJSONError("Invalid JSON response, retrying...")
        else:
            error_data = response.json()
            error_type = error_data.get("error", {}).get("type", "Unknown")
            error_message = error_data.get("error", {}).get("message", "Unknown")
            print(f"An error occurred while generating text: (Status Code: {response.status_code}, Type: {error_type}, Message: {error_message})")
            return None


    except requests.exceptions.RequestException as e:
        print(f"A request-related error occurred: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"A JSON decoding error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while generating text: {e}")
        return None

def process_input_file(input_file, system_message, assistant_message, args):
    with open(input_file, "r") as f:
        user_prompt = f.read()

    generated_text = response(prompt=None, max_tokens=args.mt, t=args.t, n=args.n, system_message=system_message, user_prompt=user_prompt, top_p=args.tp, frequency_penalty=args.fp, presence_penalty=args.pp, assistant_message=assistant_message)

    if generated_text is not None:
        output_file = f"{output_dir}/output_{int(time.time())}.json"
        with open(output_file, "w") as f:
            f.write(json.dumps(generated_text))
        print(f"Wrote output to {output_file}")
    else:
        print("Failed to generate text.")
    time.sleep(1)  # Sleep for 1 second before requesting the next chunk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smf", help="Path to input file containing system message", default="./system-messages/_Default/189_youareanailangu_1679744083")
    parser.add_argument("--amf", help="Path to input file containing assistant message", default="./prompts/assistant-messages/Default")
    parser.add_argument("--mt", type=int, help="Maximum number of tokens per request", default=4000)
    parser.add_argument("--t", type=float, help="Temperature", default=1.0)
    parser.add_argument("--n", type=int, help="Number of responses", default=1)
    parser.add_argument("--tp", type=float, help="Top_p value", default=1.0)
    parser.add_argument("--fp", type=float, help="Frequency penalty", default=0.0)
    parser.add_argument("--pp", type=float, help="Presence penalty", default=0.0)
    parser.add_argument("input_file", help="Path to input file containing prompt text", nargs='?')

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        user_prompt = f.read()

    if args.smf:
        with open(args.smf, "r") as f:
            system_message = f.read().strip()

    if args.amf:
        with open(args.amf, "r") as f:
            assistant_message = f.read().strip()
    else:
        assistant_message = None

    if os.path.isfile(args.input_file):
        # If input_file is a file, process it
        process_input_file(args.input_file, system_message, assistant_message, args)
    elif os.path.isdir(args.input_file):
        # If input_file is a directory, process each file in the directory
        input_files = os.listdir(args.input_file)
        for file in input_files:
            input_file_path = os.path.join(args.input_file, file)
            process_input_file(input_file_path, system_message, assistant_message, args)
    else:
        print("Error: Input file or directory not found.")
        exit(1)

if __name__ == "__main__":
    main()

# Merge and extract the content using the script located in the same directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["python", os.path.join(SCRIPT_DIR, "extract_merge_gpt3.5.py")])
