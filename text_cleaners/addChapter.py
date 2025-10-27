import os
import re
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")
chapterPattern = r"Chapter.+\((\d+)\)"
theChapterPattern = r"The.+\(\d+.+\).+Chapter"


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
                bracketNumber = int(isLineChapter.group(1))
                post["chapter"] = bracketNumber
                allLines.remove(line)

            if isLineTheChapter:
                allLines.remove(line)

            if isLineUppercaseTitle and line.strip():
                allLines.remove(line)

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
