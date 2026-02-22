import os
import string
import frontmatter
import readtime


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def add_title_readtime(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        all_lines = content.splitlines(keepends=True)

        post["reading_time"] = readtime.of_markdown(post.content).text

        for line in all_lines:
            if line.isupper():
                post["title"] = string.capwords(line).strip()
                all_lines.remove(line)
                break

    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
