import re
import os
import shutil

from langdetect import DetectorFactory

DetectorFactory.seed = 0

# Dòng đó có nguyên cụm "Chapter"
# sau đó là các kí tự gì ko quan tâm
# sau đó capture group là số nằm trong ()
chapter_pattern = r"Chapter.+\((\d+)\)"
# Dòng đó có chữ The và Chapter
# lấy cái số nằm trong ()
the_chapter_pattern = r"The.+\((\d+).+\).+Chapter"

save_path = r"D:\Projects\ay_gogh\test"
exclude_char = ["—", "...", ". . ."]

""" 
- Detect nếu dòng đó chứa "Chapter" và (n)
- Lưu dòng đó và các dòng ở dưới nó cho đến dòng chứa "Chapter" và (n+1)
"""


def delete_test_files(path):
    shutil.rmtree(path)
    os.mkdir(path)


def isLineSkippable(line):
    isSkippable = False

    if line.strip().isdigit():
        isSkippable = True

    for char in exclude_char:
        if char in line:
            isSkippable = True
            break

    return isSkippable


def split_chapters(input_file):
    curr_chap = 0

    with open(input_file, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    for line in content:
        if isLineSkippable(line):
            continue

        # Determine if the line include "Chapter" and (n)
        chapter_match = re.match(chapter_pattern, line)

        if chapter_match:
            if chapter_match.group(1) != curr_chap:
                curr_chap = chapter_match.group(1)
            else:
                continue

        output_file = os.path.join(save_path, f"{curr_chap}.md")
        with open(output_file, "a", encoding="utf-8") as out:
            out.writelines(line)


if __name__ == "__main__":
    delete_test_files(save_path)
    split_chapters("full.txt")
