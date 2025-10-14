import re
import os
import shutil
from tqdm import tqdm

# Dòng đó có nguyên cụm "Chapter"
# sau đó là các kí tự gì ko quan tâm
# sau đó capture group là số nằm trong ()
chapterPattern = r"Chapter.+\((\d+)\)"

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")

""" 
- Detect nếu dòng đó chứa "Chapter" và (n)
- Lưu dòng đó và các dòng ở dưới nó cho đến dòng chứa "Chapter" và (n+1)
"""

"""
AI code quá khó hiểu, đã vậy còn chả đúng
"""


def deleteTestFiles(path):
    shutil.rmtree(path)
    os.mkdir(path)


def splitChapter(inputFile, testNumber = None):
    currentChapter = 0

    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    for line in tqdm(content):
        if testNumber is not None and currentChapter == testNumber + 1:
            break

        # Determine if the line include "Chapter" and (n)
        isLineChapter = re.match(chapterPattern, line)

        if isLineChapter:
            bracketNumber = int(isLineChapter.group(1))
            if bracketNumber != currentChapter:
                currentChapter = bracketNumber
            # The same "Chapter (n)"" line occurs again !
            else:
                continue

        outputFile = os.path.join(savePath, f"{currentChapter}.txt")
        with open(outputFile, "a", encoding="utf-8") as out:
            out.writelines(line)


if __name__ == "__main__":
    deleteTestFiles(savePath)
    splitChapter("full.txt")
