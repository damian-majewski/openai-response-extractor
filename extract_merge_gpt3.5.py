import json
import argparse
import os
import glob
import shutil

# Determine the repository base directory from the location of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(BASE_DIR, "outputs")
extracts_dir = os.path.join(BASE_DIR, "extracts")
input_dir = os.path.join(BASE_DIR, "responses")

# Create directories if they do not exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(extracts_dir, exist_ok=True)

def extract_text(input_file):
    texts = []
    with open(input_file, "r") as f:
        data = json.load(f)

        choices = data["choices"]  # Access 'choices' directly from the data dictionary
        for choice in choices:
            # Updated this line to access the message content correctly
            message = choice["message"]
            if message["role"] == "assistant":
                text = message["content"].replace("\n\n", "\n")
                texts.append(text.strip())

    return texts

def get_newest_file(input_dir):
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    if len(files) > 0:
        newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(input_dir, f)))
        return newest_file
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Path to input file")
    args = parser.parse_args()

    # Check input file or get the latest response
    if args.input_file and os.path.exists(args.input_file):
        input_file = args.input_file
        print(f"Processing file: {input_file}") # Debugging line
    else:
        newest_file = get_newest_file(input_dir)
        if newest_file is not None:
            input_file = os.path.join(input_dir, newest_file)
            print(f"Processing file: {input_file}") # Debugging line
        else:
            print("No files found in the input directory.")
            exit(1)

    texts = extract_text(input_file)

    # Save extracted texts to individual files
    input_basename = os.path.basename(input_file).split("_", 1)[1]
    input_name, input_ext = os.path.splitext(input_basename)
    for i, text in enumerate(texts):
        output_file = os.path.join(output_dir, f"extract_{input_name}_{i}{input_ext}")
        with open(output_file, "w") as f:
            f.write(text)
    
    # Merge extracted texts into a single file
    merged_file = os.path.join(extracts_dir, f"merged_extracted_{input_name}{input_ext}")

    # Get the list of individual files and sort them
    individual_files = glob.glob(os.path.join(output_dir, f"extract_{input_name}_*{input_ext}"))
    print(f"Individual files: {individual_files}") # Debugging line
    sorted_files = sorted(individual_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    # Merge the individual files in the sorted order
    with open(merged_file, "w") as f:
        for file in sorted_files:
            with open(file, "r") as infile:
                f.write(infile.read() + "\n\n")

    # Cleanup 
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        # Check if it is a file (not a directory)
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)
        elif os.path.isdir(file_path):
            # Remove the directory and its contents
            shutil.rmtree(file_path)