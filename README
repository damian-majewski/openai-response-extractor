# OpenAI Response Extractor

## Features
- Call the OpenAI ChatGPT API with custom prompts
- Extract and save the generated text from API responses
- Save individual generated text snippets to separate output files
- Merge extracted texts into a single output file
- Simple command-line interface for running the scripts

## Prerequisites

- Python 3.6 or later
- An OpenAI API key (set as an environment variable `OPENAI_API_KEY`)

### Using direnv to manage environment variables
We recommend using direnv to manage your environment variables, including your OpenAI API key. This tool allows you to set up project-specific environment variables, which will be automatically loaded when you enter the project directory.

To set up direnv:

1. Install direnv by following the instructions on the official website.
2. In the root of the cloned repository, create a .envrc file.
3. Add the following line to the .envrc file, replacing <YOUR_API_KEY> with your actual OpenAI API key:
export OPENAI_API_KEY="<YOUR_API_KEY>"

4. Allow direnv to load the environment variables from the .envrc file by running:
direnv allow

## Setup environment
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


## Installation

1. Clone this repository or download the script.
2. Install the required packages by running `python -m pip install -r requirements.txt`.


## Directories

- `./extracts`: Directory for extracted response.
- `./outputs`: Directory for storing the generated output files.
- `./responses`: Directory for responses.


# Usage OpenAI Response Extractor

## Send API call with file
python request_api.py prompts/text_file 
python request_api.py --n 5 --t 0.7 prompts/text_file 

## Extract and merge the output
python extract_merge.py - without argument will extract latest response file
python extract_merge.py responses/output_1679591528.json - will extract file from the path