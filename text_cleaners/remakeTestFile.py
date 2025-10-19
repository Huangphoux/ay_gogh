from splitChapter import deleteTestFiles, splitChapter
from addCodeBlock import addCodeBlock
from changeFileExtension import changeFileExtension
from addHeading import addHeading
from deleteLine import deleteLine
from deleteCodeBlock import deleteCodeBlock
from generateAudio import TTSProcessor, generateTTS

import os
from tqdm import tqdm

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")
weirdPath = os.path.join(os.path.dirname(__file__), "weirdList.txt")
fullPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "full.txt")


def remakeTestFile():
    deleteTestFiles(savePath)
    print("Deleted test files.")

    os.remove(weirdPath)
    
    print("Splitting chapters:")

    splitChapter(fullPath, 20)

    # tts = TTSProcessor()

    for root, _, files in os.walk(savePath):
        print("Processing on each file:")

        for filename in tqdm(files):
            filePath = os.path.join(root, filename)
            try:
                deleteLine(filePath)

                # generateTTS(filePath, tts)

                addHeading(filePath)
                addCodeBlock(filePath)
                deleteCodeBlock(filePath)

                changeFileExtension(filePath)

            except Exception as e:
                print(f"Error!! {filename}: {str(e)}")


if __name__ == "__main__":
    remakeTestFile()
