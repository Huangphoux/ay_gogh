from splitChapter import deleteTestFiles, splitChapter
from addCodeBlock import addCodeBlock
from addHeading import addHeading
from deleteLine import deleteLine
from deleteCodeBlock import deleteCodeBlock

import os
from tqdm import tqdm

rootProjectPath = os.path.dirname(os.path.dirname(__file__))

savePath = os.path.join(rootProjectPath, "test")
weirdPath = os.path.join(rootProjectPath, "weird_line.txt")
fullPath = os.path.join(rootProjectPath, "full.txt")


def remakeTestFile():
    deleteTestFiles(savePath)
    print("Deleted test files.")
    
    if os.path.exists(weirdPath):
        os.remove(weirdPath)

    splitChapter(fullPath)

    for root, _, files in os.walk(savePath):
        print("Processing on each file:")

        for filename in tqdm(files):
            filePath = os.path.join(root, filename)
            try:
                deleteLine(filePath)

                addHeading(filePath)
                addCodeBlock(filePath)
                deleteCodeBlock(filePath)

            except Exception as e:
                print(f"Error!! {filename}: {str(e)}")


if __name__ == "__main__":
    remakeTestFile()
