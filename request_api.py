import openai
import json
import time
import argparse
import os
import subprocess

# Directory to save output files
output_dir = "./responses"  

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Function to generate response
def response(prompt, max_tokens, t, n, model="text-davinci-002"):
    try:
        chunks = [prompt[i:i+max_tokens] for i in range(0, len(prompt), max_tokens)]
        responses = []
        for chunk in chunks:
            response = openai.Completion.create(
                engine=model,
                prompt=chunk,
                n=n,
                max_tokens=max_tokens,
                stop=None,
                temperature=t,
                #stream=True,
            )
            responses.append(response)
        return responses
    except openai.OpenAIError as e:
        print(f"An error occurred while generating text: {e}")
        return None


# Parsing input file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file containing prompt text")
    parser.add_argument("--max_tokens", type=int, help="Maximum number of tokens per request", default=2048)
    parser.add_argument("--t", type=float, help="Temperature", default=0.5)
    parser.add_argument("--n", type=int, help="Number of pages", default=10)

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        prompt = f.read()

    # Invoke function to get response
    generated_text = response(prompt, max_tokens=args.max_tokens, t=args.t, n=args.n)
    if generated_text is not None:
        output_file = f"{output_dir}/output_{int(time.time())}.json"
        with open(output_file, "w") as f:
            f.write(json.dumps(generated_text))
        print(f"Wrote output to {output_file}")
    else:
        print("Failed to generate text.")
    time.sleep(1)  # Sleep for 1 second before requesting the next chunk

# Merge and extract the content
subprocess.run(["python", "./extract_merge.py"])