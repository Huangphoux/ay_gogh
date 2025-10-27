import os
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")
chapterPattern = r"Chapter.+\((\d+)\)"


def addReadability(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        
        

        post[item.__name__] = number

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
