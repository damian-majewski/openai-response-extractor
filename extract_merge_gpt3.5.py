import json
import argparse
import os
import glob
import shutil

output_dir = "./outputs"
extracts_dir = "./extracts"
input_dir = './responses'  # Replace this with the path to your input directory

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
    newest_file = get_newest_file(input_dir)
    if newest_file is not None:
        args.input_file = os.path.join(input_dir, newest_file)
    else:
        print("No files found in the input directory.")
        exit(1)
    

    texts = extract_text(args.input_file)

    # Save extracted texts to individual files
    input_basename = os.path.basename(args.input_file)
    input_name, input_ext = os.path.splitext(input_basename)
    for i, text in enumerate(texts):
        output_file = f"{output_dir}/extract_{input_name}_{i}{input_ext}"
        with open(output_file, "w") as f:
            f.write(text)
    
    # Merge extracted texts into a single file
    merged_file = f"{extracts_dir}/merged_extracted_{input_name}{input_ext}"
    
    # Get the list of individual files and sort them
    individual_files = glob.glob(f"{output_dir}/extract_{input_name}_*{input_ext}")
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