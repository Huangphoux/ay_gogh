import os
from tqdm import tqdm


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addCodeBlock(inputFile):
    # First read the content
    with open(inputFile, mode="r", encoding="utf-8") as f:
        allLines = f.readlines()
        first3Lines = allLines[:3]
        content = allLines[3:]

        # Skip empty files
        if not content:
            return

        # Length of the longest line
        maxLineLength = len(max(content, key=len))

    # Then write the processed content
    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in first3Lines:
            f.write(line)

        isCodeBlockOpen = False

        for line in content:
            if len(line.strip()) <= maxLineLength // 3:
                if not isCodeBlockOpen:
                    isCodeBlockOpen = True
                    f.write("```\n")
            else:
                if isCodeBlockOpen:
                    isCodeBlockOpen = False
                    f.write("```\n")

            f.write(line)

        # Close any remaining open code block
        if isCodeBlockOpen:
            f.write("```\n")


if __name__ == "__main__":
    for root, _, files in os.walk(savePath):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                addCodeBlock(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
