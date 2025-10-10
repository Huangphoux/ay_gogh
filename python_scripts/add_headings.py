import os
from tqdm import tqdm


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def add_headings(input_file):
    # First read the content
    with open(input_file, mode="r", encoding="utf-8") as f:
        all_lines = f.readlines()
        first_three_lines = all_lines[:3]
        content = all_lines[3:]

        # Skip empty files
        if not content:
            return

    # Then write the processed content
    with open(input_file, mode="w", encoding="utf-8") as f:
        for line in first_three_lines:
            f.write("# " + line)

        for line in content:
            if "WORDS" in line:
                f.write("# Words")
                continue
            
            f.write(line)


if __name__ == "__main__":
    for root, _, files in os.walk(save_path):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                add_headings(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
