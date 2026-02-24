import re
import os
import shutil

# Dòng đó có nguyên cụm "Chapter"
# sau đó là các kí tự gì ko quan tâm
# sau đó capture group là số nằm trong ()
chapter_regex = r"Chapter.+\((\d+)\)"

root_path = os.path.dirname(os.path.dirname(__file__))

save_path = os.path.join(root_path, "test")


def remove_test(path):
    shutil.rmtree(path)
    os.mkdir(path)


def split_chapter(inputFile, test_num=None):
    curr_chap = 0

    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    for line in content:
        # Stop at chapter (testNumber)+1
        if test_num is not None and curr_chap == test_num + 1:
            break

        # is line "Chapter" and (n) ?
        is_chapter = re.match(chapter_regex, line)

        if is_chapter:
            num_bracket = int(is_chapter.group(1))

            if num_bracket != curr_chap:
                curr_chap = num_bracket
            else:  # "Chapter (n)"" appears again !
                continue

        output = os.path.join(save_path, f"{curr_chap}.md")
        with open(output, "a", encoding="utf-8") as out:
            out.writelines(line)
