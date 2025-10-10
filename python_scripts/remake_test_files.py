from split_chapters import delete_test_files, split_chapters
from detect_marginal_notes import detect_marginal_notes
from change_to_md import change_to_md
from add_headings import add_headings
from detect_non_english_lines import detect_non_english

import os
from tqdm import tqdm

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def main():
    delete_test_files(save_path)
    print("Deleted test files.")
    print("Splitting chapters:")
    
    split_chapters("full.txt")

    for root, _, files in os.walk(save_path):
        print("Processing on each file:")

        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                detect_non_english(file_path)
                # print("Add headings:")
                add_headings(file_path)
                # print("Detect marginal notes:")
                detect_marginal_notes(file_path)
                # print("Change file extension to .md:")
                change_to_md(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


if __name__ == "__main__":
    main()
