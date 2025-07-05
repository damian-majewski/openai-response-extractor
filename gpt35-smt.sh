# Usage: gpt35-smt my_system_message.txt 2000 0.8 3 my_input_prompt.txt my_assistant_message.txt 0.5 0.2
# Define the path to the git repo
# Define the prefix directory variable
read -p "Enter the prefix directory for the prompts and system messages: " prefix_dir
export PROMPT_DIR="${prefix_dir}/prompts"
export SYSTEM_MSG_DIR="${prefix_dir}/system-messages"

# Define the function
function gpt35-smt() {
  system_message_filename="$1"
  max_tokens="$2"
  t="$3"
  n="$4"
  input_file="$5"
  assistant_message_filename="$6"
  top_p="$7"
  frequency_penalty="$8"
  presence_penalty="${9:-0.0}"

  # Check if the given file path is a valid file
  is_valid_file() {
    local file="$1"
    local dir="$2"
    if [ -f "$file" ]; then
      echo "$file"
    else
      local file_path="${dir}/${file}"
      if [ -f "$file_path" ]; then
        echo "$file_path"
      else
        echo ""
      fi
    fi
  }


  # Search for the files in the directories of your choice only if the given path is not a valid file
  system_message_filepath=$(is_valid_file "${system_message_filename}" "${SYSTEM_MSG_DIR}")
  if [ -z "${system_message_filepath}" ]; then
    system_message_filepath=$(find "${SYSTEM_MSG_DIR}" -name "${system_message_filename}" -exec sh -c 'echo {}' \; | tail -1)
  fi
  
  input_filepath=$(is_valid_file "${input_file}" "${PROMPT_DIR}")
  if [ -z "${input_filepath}" ]; then
    input_filepath=$(find "${PROMPT_DIR}" -name "${input_file}" -exec sh -c 'echo {}' \; | tail -1)
  fi
  
  assistant_message_filepath=$(is_valid_file "${assistant_message_filename}" "${PROMPT_DIR}/assistant-messages")
  if [ -z "${assistant_message_filepath}" ]; then
    assistant_message_filepath=$(find "${PROMPT_DIR}/assistant-messages" -name "${assistant_message_filename}" -exec sh -c 'echo {}' \; | tail -1)
  fi

  echo "System message file path: ${system_message_filepath}"
  echo "Input file path: ${input_filepath}"
  echo "Assistant message file path: ${assistant_message_filepath}"

  # Determine the directory where this script resides to locate the Python helper
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  python "${script_dir}/request_api_gpt3.5.py" \
    --smf "${system_message_filepath}" \
    --mt "${max_tokens}" \
    --t "${t}" \
    --n "${n}" \
    --amf "${assistant_message_filepath}" \
    --tp "${top_p}" \
    --fp "${frequency_penalty}" \
    --pp "${presence_penalty}" \
    "${input_filepath}"
}

# Add the function to .bashrc or .bash_profile
echo "source /path/to/gpt35-smt-bash-function.sh" >> ~/.bashrc  # or ~/.bash_profile if using macOS