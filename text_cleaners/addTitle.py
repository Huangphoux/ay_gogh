import os
import string
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addTitle(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        allLines = content.splitlines(keepends=True)

        for line in allLines:
            if line.isupper():
                post["title"] = string.capwords(line).strip()
                break

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
