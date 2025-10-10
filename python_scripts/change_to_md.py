import os
from tqdm import tqdm

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def change_to_md(input_file):
    if input_file.endswith(".txt"):
        new_file = input_file.replace(".txt", ".md")
        
        try:
            os.rename(input_file, new_file)
        except OSError as e:
            print(f"Error renaming {input_file}: {str(e)}")


if __name__ == "__main__":
    for root, _, files in os.walk(save_path):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                change_to_md(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
