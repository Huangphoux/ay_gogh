from splitChapter import deleteTestFiles, splitChapter
from addCodeBlock import addCodeBlock
from addHeading import addHeading
from deleteLine import deleteLine
from deleteCodeBlock import deleteCodeBlock
from addReadTime import addReadTime
from addCEFR import addCEFR
from addTitle import addTitle
from addReadability import addReadability
from addChapter import addChapter
from profiler import profile_step, profile_remake

import os
from tqdm import tqdm

rootProjectPath = os.path.dirname(os.path.dirname(__file__))

savePath = os.path.join(rootProjectPath, "test")
weirdPath = os.path.join(rootProjectPath, "weird_line.txt")
fullPath = os.path.join(rootProjectPath, "full.txt")

# Wrap processing steps with profiler
deleteLine = profile_step(deleteLine)
addReadability = profile_step(addReadability)
addHeading = profile_step(addHeading)
addChapter = profile_step(addChapter)
addTitle = profile_step(addTitle)
addReadTime = profile_step(addReadTime)
addCEFR = profile_step(addCEFR)
addCodeBlock = profile_step(addCodeBlock)
deleteCodeBlock = profile_step(deleteCodeBlock)


@profile_remake
def remakeTestFile():
    deleteTestFiles(savePath)
    print("Deleted test files.")

    if os.path.exists(weirdPath):
        os.remove(weirdPath)

    splitChapter(fullPath, 20)

    for root, _, files in os.walk(savePath):
        print("Processing on each file:")

        for filename in tqdm(files):
            filePath = os.path.join(root, filename)
            try:
                steps = [
                    deleteLine,
                    addReadability,
                    addHeading,
                    addChapter,
                    addTitle,
                    addReadTime,
                    # addCEFR,
                    addCodeBlock,
                    deleteCodeBlock,
                ]

                for step in steps:
                    step(filePath)

            except Exception as e:
                print(f"{e.__class__.__name__}: {filename}: {str(e)}")


if __name__ == "__main__":
    remakeTestFile()
