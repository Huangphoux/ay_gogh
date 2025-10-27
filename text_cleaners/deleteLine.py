import os
import re

rootProjectPath = os.path.dirname(os.path.dirname(__file__))

savePath = os.path.join(rootProjectPath, "test")
weirdPath = os.path.join(rootProjectPath, "weird_line.txt")
banPath = os.path.join(rootProjectPath, "ban_list.txt")

# Initialize global exclude_char list
banList = []

# Dòng đó có chữ The và Chapter
# lấy cái số nằm trong ()
theChapterPattern = r"The.+\(\d+.+\).+Chapter"


def loadBanList():
    global banList

    try:
        with open(banPath, mode="r", encoding="utf-8") as f:
            banList = [line.strip() for line in f]
    except FileNotFoundError:
        print("Warning: ban_list.txt not found")


def isLineSkippable(line):
    s = line.strip()
    if s.isdigit():
        return True
    for item in banList:
        if item in s:
            return True
    try:
        int(s)
        return True
    except ValueError:
        return False


def deleteLine(inputFile):
    loadBanList()

    weirdList = []

    with open(inputFile, mode="r", encoding="utf-8") as f:
        allLines = f.readlines()
        content = allLines

    with open(inputFile, mode="w", encoding="utf-8") as f:
        hasTheChapterAppeared = False

        for line in content:
            isLineTheChapter = re.match(theChapterPattern, line)

            if isLineTheChapter:
                if not hasTheChapterAppeared:
                    hasTheChapterAppeared = True
                else:
                    continue

            if isLineSkippable(line):
                weirdList.append(line)
                continue

            f.write(line)

    with open(weirdPath, mode="a+", encoding="utf-8") as f:
        for item in weirdList:
            f.write(item)


def makeWeirdString(tabNum):
    weirdString = ""
    for _ in range(tabNum):
        weirdString += "\t"
    weirdString += "WEIRD"
    for _ in range(tabNum):
        weirdString += "\t"
    return weirdString
