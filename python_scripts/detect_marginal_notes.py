import os
from tqdm import tqdm


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def detect_marginal_notes(input_file):
    # First read the content
    with open(input_file, mode="r", encoding="utf-8") as f:
        all_lines = f.readlines()
        first_three_lines = all_lines[:3]
        content = all_lines[3:]

        # Skip empty files
        if not content:
            return

        # Length of the longest line
        longest_length = len(max(content, key=len))

    # Then write the processed content
    with open(input_file, mode="w", encoding="utf-8") as f:
        for line in first_three_lines:
            f.write(line)
        
        has_open_code_block = False

        for line in content:
            if len(line.strip()) <= longest_length // 3:
                if not has_open_code_block:
                    has_open_code_block = True
                    f.write("```\n")
            else:
                if has_open_code_block:
                    has_open_code_block = False
                    f.write("```\n")

            f.write(line)

        # Close any remaining open code block
        if has_open_code_block:
            f.write("```\n")


if __name__ == "__main__":
    for root, _, files in os.walk(save_path):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                detect_marginal_notes(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
