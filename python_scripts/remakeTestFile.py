from splitChapter import deleteTestFiles, splitChapter
from addCodeBlock import addCodeBlock
from changeFileExtension import changeFileExtension
from addHeading import addHeading
from deleteLine import deleteLine

import os
from tqdm import tqdm

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def main():
    deleteTestFiles(savePath)
    print("Deleted test files.")
    print("Splitting chapters:")

    splitChapter("full.txt", 10)

    for root, _, files in os.walk(savePath):
        print("Processing on each file:")

        for filename in tqdm(files):
            filePath = os.path.join(root, filename)
            try:
                deleteLine(filePath)
                # print("Add headings:")
                addHeading(filePath)
                # print("Detect marginal notes:")
                addCodeBlock(filePath)
                # print("Change file extension to .md:")
                changeFileExtension(filePath)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


if __name__ == "__main__":
    main()
