import os
import readtime
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addReadTime(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        read_time = readtime.of_markdown(post.content).text
        post["read-time"] = read_time

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
