import re
import os
import shutil
from tqdm import tqdm

# Dòng đó có nguyên cụm "Chapter"
# sau đó là các kí tự gì ko quan tâm
# sau đó capture group là số nằm trong ()
chapterPattern = r"Chapter.+\((\d+)\)"

rootProjectPath = os.path.dirname(os.path.dirname(__file__))

savePath = os.path.join(rootProjectPath, "test")


def deleteTestFiles(path):
    shutil.rmtree(path)
    os.mkdir(path)


def splitChapter(inputFile, testNumber=None):
    currentChapter = 0

    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    for line in tqdm(content):
        # Stop at chapter (testNumber)+1
        if testNumber is not None and currentChapter == testNumber + 1:
            break

        # check if the line is "Chapter" and (n)
        isLineChapter = re.match(chapterPattern, line)

        if isLineChapter:
            bracketNumber = int(isLineChapter.group(1))

            if bracketNumber != currentChapter:
                currentChapter = bracketNumber
            else:  # The same "Chapter (n)"" line occurs again !
                continue

        outputFile = os.path.join(savePath, f"{currentChapter}.md")
        with open(outputFile, "a", encoding="utf-8") as out:
            out.writelines(line)


if __name__ == "__main__":
    deleteTestFiles(savePath)
    splitChapter("full.txt")
