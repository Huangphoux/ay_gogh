from split_chapter import remove_test, split_chapter
from add_code_block import add_code_block
from delete_line import delete_line
from delete_code_block import delete_code_block
from add_cefr import add_cefr
from add_title_readtime import add_title_readtime
from add_readability import add_readability
from add_chapter import add_chapter
from profiler import profile_step, profile_remake

import os
from tqdm import tqdm

root_path = os.path.dirname(os.path.dirname(__file__))

save_path = os.path.join(root_path, "test")
weird_path = os.path.join(root_path, "weird_line.txt")
full_path = os.path.join(root_path, "full.txt")

# Wrap processing steps with profiler
delete_line = profile_step(delete_line)
add_readability = profile_step(add_readability)
add_chapter = profile_step(add_chapter)
add_title_readtime = profile_step(add_title_readtime)
add_cefr = profile_step(add_cefr)
add_code_block = profile_step(add_code_block)
delete_code_block = profile_step(delete_code_block)

test_number = 40


@profile_remake
def clean_text():
    remove_test(save_path)
    print("Deleted test files.")

    if os.path.exists(weird_path):
        os.remove(weird_path)

    split_chapter(full_path, test_number)

    for root, _, files in os.walk(save_path):
        print("Processing on each file:")

        for fname in tqdm(files):
            fpath = os.path.join(root, fname)
            try:
                steps = [
                    delete_line,
                    add_readability,
                    add_chapter,
                    add_title_readtime,
                    # addCEFR,
                    add_code_block,
                    delete_code_block,
                ]

                for step in steps:
                    step(fpath)

            except Exception as e:
                print(f"{e.__class__.__name__}: {fname}: {str(e)}")

        # Remove preface
        os.remove(os.path.join(save_path, "0.md"))
        # Remove useless n+1 file
        os.remove(os.path.join(save_path, f"{test_number + 1}.md"))


if __name__ == "__main__":
    clean_text()
