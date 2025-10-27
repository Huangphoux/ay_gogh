import os

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addCodeBlock(inputFile):
    # First read the content
    with open(inputFile, mode="r", encoding="utf-8") as f:
        allLines = f.readlines()

        # Skip frontmatter (YAML between --- markers)
        frontmatterEnd = 0
        if allLines and allLines[0].strip() == "---":
            for i in range(1, len(allLines)):
                if allLines[i].strip() == "---":
                    frontmatterEnd = i + 1
                    break

        frontmatter = allLines[:frontmatterEnd]
        content = allLines[frontmatterEnd:]

        # Skip empty files
        if not content:
            return

        # Length of the longest line
        maxLineLength = len(max(content, key=len))

    # Then write the processed content
    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in frontmatter:
            f.write(line)

        isCodeBlockOpen = False

        for line in content:
            if len(line.strip()) < maxLineLength / 3:
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
