import os
import re
from tqdm import tqdm
from langdetect import detect

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")

# Initialize global exclude_char list
banList = []

# Dòng đó có chữ The và Chapter
# lấy cái số nằm trong ()
theChapterPattern = r"The.+\(\d+.+\).+Chapter"


def loadBanList():
    global banList

    banListFile = os.path.join(os.path.dirname(__file__), "ban_list.txt")

    try:
        with open(banListFile, mode="r", encoding="utf-8") as f:
            banList = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Warning: ban_list.txt not found")


def isLineSkippable(line):
    if line.strip().isdigit():
        return True

    for item in banList:
        if item in line:
            return True


def deleteLine(inputFile):
    loadBanList()

    with open(inputFile, mode="r", encoding="utf-8") as f:
        allLines = f.readlines()
        content = allLines

        # Skip empty files
        if not content:
            return

        maxLineLength = len(max(content, key=len))

    # Then write the processed content
    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in content:
            if isLineSkippable(line):
                continue
            
            try:
                isLineShort = len(line.strip()) <= maxLineLength // 3
                isLineEnglish = detect(line.strip()) == "en"

                if isLineShort or isLineEnglish:
                    f.write(line)
                    continue

                tabNumber = 6
                weirdString = ""
                for _ in range(tabNumber):
                    weirdString += "\t"
                weirdString += "WEIRD"
                for _ in range(tabNumber):
                    weirdString += "\t"

                f.write(weirdString + line)
            except Exception:
                f.write(weirdString + line)


if __name__ == "__main__":
    # Load the non-English characters
    loadBanList()
    print(banList)

    for root, _, files in os.walk(savePath):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                deleteLine(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
