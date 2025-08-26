# OpenAI Response Extractor
This repository provides a simple implementation to extract content from OpenAI's GPT using OpenAI API. The provided Bash alias function simplifies the usage of the Python script.

## Features
- Call the OpenAI ChatGPT API with custom prompts
- Extract and save the generated text from API responses
- Save individual generated text snippets to separate output files
- Merge extracted texts into a single output file
- Simple command-line interface for running the scripts
# Usage OpenAI Response Extractor

## Using the Bash Alias Function
The Bash alias function simplifies the usage of the Python script by providing a more convenient way to call the script with the necessary parameters.
1. Add the gpt35-smt function from gpt35-smt.sh to your .bashrc or .bash_profile file.
2. Replace <path_to_repo> in the prefix variable with the path to this repository on your local machine.
3. Use the gpt35-smt function as follows: 
`gpt35-smt "system_message_filename" max_tokens temperature n "input_file_with_prompt" "assistant_message_file" top_p frequency_penalty presence_penalty`
### Example:
`gpt35-smt "/path/to/playbook_expert_message" 1000 1.0 3 "/path/to/prompt/example_playbook_idea" "/path/to/assistan-message-playbook-creation" 1.0 0.0 0.0`

## Using the Python Script
You can also use the Python script directly by running the request_api_gpt3.5.py script:
`python request_api_gpt3.5.py --smf "system_message_filepath" --mt max_tokens --t temperature --n n --amf "assistant_message_filepath" --tp top_p --fp frequency_penalty --pp presence_penalty "input_filepath"`

The final positional argument `input_filepath` is **required** and should point to the prompt file or directory.

### Example:
`python request_api_gpt3.5.py --smf "./system-messages/Technology/ansible_playbook" --mt 1000 --t 1.0 --n 3 --amf "./prompts/assistant-messages/Technology/ansible" --tp 1.0 --fp 0.0 --pp 0.0 "./prompts/ansible_playbook"`

### Notes
- The `max_tokens` parameter controls the maximum number of tokens generated in the response. A higher value will return more content, but may consume more tokens from your API quota.
- The `temperature` parameter controls the randomness of the output. Lower values (e.g., 0.2) will produce more focused and deterministic output, while higher values (e.g., 1.0) will produce more diverse and creative output.
- The `n` parameter controls the number of responses generated.
- The `top_p` parameter controls the nucleus sampling technique. A value of 1.0 will use all tokens in the distribution, while lower values (e.g., 0.9) will only use the most probable tokens. Adjusting this value can impact the output's diversity and quality.
- The `frequency_penalty` parameter can be used to control the repetition of tokens in the generated text. Negative values (e.g., -1.0) will encourage more frequent words, while positive values (e.g., 1.0) will encourage less frequent words.
- The `presence_penalty` parameter can be used to control the repetition of topics in the generated text. Negative values (e.g., -1.0) will encourage more repetition of topics, while positive values (e.g., 1.0) will encourage less repetition of topics.

Please note that the Bash alias function is provided to simplify the usage of the Python script by providing a more convenient way to call the script with the necessary parameters. This function is not required to run the Python script but offers a more user-friendly interface for interacting with the script.

## Directories

- `./extracts`: Directory where the extracted and merged content from the responses will be saved.
- `./system-messages`: Directory containing system messages to be used as a context for GPT-3.5 Turbo.
- `./responses`: Directory where the generated JSON files containing GPT-3.5 Turbo responses will be saved.
- `./prompts`: Directory containing user prompts and assistant messages.

## Merging and Extracting Content
After generating the responses, you can merge and extract the content using the extract_merge_gpt3.5.py script:

`python extract_merge_gpt3.5.py`
This script will combine the generated responses and extract the content from the JSON files saved in the responses directory, and save the extracted content in the extracts directory.

## Prerequisites

- Python 3.6 or later
- An OpenAI API key (set as an environment variable `OPENAI_API_KEY`)

### Setup environment
1. Check the Python interpreter
which python
which python3

2. Install virtualenv globally
python -m pip install virtualenv

3. Create and navigate to the project directory
cd <project_directory>

4. Create a virtual environment for your project
virtualenv <virtualenv_name>

5. Activate the virtual environment
source <virtualenv_name>/bin/activate

6. Install dependencies in the virtual environment
python -m pip install -r requirements.txt

7. Run the script
python script.py input_file.txt

8. Deactivate the virtual environment when you're done
deactivate

### (Optional) Using direnv to manage environment variables
We recommend using direnv to manage your environment variables, including your OpenAI API key. This tool allows you to set up project-specific environment variables, which will be automatically loaded when you enter the project directory.

To set up direnv:

1. Install direnv by following the instructions on the official website.
2. In the root of the cloned repository, create a .envrc file.
3. Add the following line to the .envrc file, replacing <YOUR_API_KEY> with your actual OpenAI API key: `export OPENAI_API_KEY="<YOUR_API_KEY>"`
4. Allow direnv to load the environment variables from the .envrc file by running:
direnv allow

## Installation

1. Clone this repository or download the script.
2. Install the required packages by running `python -m pip install -r requirements.txt`.

## Contributing
If you'd like to contribute to this project, please feel free to submit a pull request or open an issue with your suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.