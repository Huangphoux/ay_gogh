import os
import re
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")
chapterPattern = r"Chapter (.+) \((\d+)\)"
theChapterPattern = r"The (.+) \((\d+.+)\).+Chapter"

# extract the number word, cardinal number, cardinal number word


def addChapter(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        allLines = content.splitlines(keepends=True)

        for line in allLines[:]:
            isLineChapter = re.match(chapterPattern, line)
            isLineTheChapter = re.match(theChapterPattern, line)
            isLineUppercaseTitle = re.match(r"^[A-Z\s]+$", line.strip())

            if isLineChapter:
                number_word = isLineChapter.group(1)
                number = int(isLineChapter.group(2))

                post["number_word"] = number_word
                post["number"] = number

                allLines.remove(line)

            if isLineTheChapter:
                cardinal_word = isLineTheChapter.group(1)
                cardinal_number = isLineTheChapter.group(2)

                post["cardinal_word"] = cardinal_word
                post["cardinal_number"] = cardinal_number

                allLines.remove(line)

            if isLineUppercaseTitle and line.strip():
                allLines.remove(line)

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
