import os

from split_chapter import remove_test, split_chapter
from add_code_block import add_code_block
from delete_line import delete_line
from delete_code_block import delete_code_block
from add_frontmatter import add_frontmatter
from remove_linebreak import remove_linebreak
from add_ngsl_level import add_ngsl_level
from fix_spelling import fix_spelling
from split_paragraph import split_paragraph


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
    os.remove(os.path.join(save_path, "0.md"))  # Remove preface

    if test_number < 60:  # Remove useless n+1 file
        os.remove(os.path.join(save_path, f"{test_number + 1}.md"))

    for root, _, files in os.walk(save_path):
        for fname in files:
            fpath = os.path.join(root, fname)

            steps = [
                delete_line,
                add_frontmatter,
                add_code_block,
                delete_code_block,
                remove_linebreak,
                fix_spelling,
                add_ngsl_level,
                split_paragraph,
            ]

            for step in steps:
                step(fpath)


if __name__ == "__main__":
    clean_text()
