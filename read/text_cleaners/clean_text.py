from split_chapter import remove_test, split_chapter
from add_code_block import add_code_block
from delete_line import delete_line
from delete_code_block import delete_code_block
from add_frontmatter import add_frontmatter

import os

root_path = os.path.dirname(os.path.dirname(__file__))

save_path = os.path.join(root_path, "chapter")
weird_path = os.path.join(root_path, "weird_line.txt")
full_path = os.path.join(root_path, "full.txt")

test_number = 70


def clean_text():
    remove_test(save_path)

    if os.path.exists(weird_path):
        os.remove(weird_path)

    split_chapter(full_path, test_number)

    for root, _, files in os.walk(save_path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                steps = [
                    delete_line,
                    add_frontmatter,
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
        # os.remove(os.path.join(save_path, f"{test_number + 1}.md"))


if __name__ == "__main__":
    clean_text()
