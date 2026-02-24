import os
import re
import frontmatter
import string


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")
chapter_regex = r"Chapter (.+) \((\d+)\)"
the_chapter_regex = r"The (.+) \((\d+.+)\).+Chapter"


def add_frontmatter(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        all_lines = content.splitlines(keepends=True)

        for line in all_lines[:]:
            if line.isupper() and ":" not in line:
                post["title"] = string.capwords(line).strip()
                all_lines.remove(line)

            is_line_chapter = re.match(chapter_regex, line)
            is_line_the_chapter = re.match(the_chapter_regex, line)

            if is_line_chapter:
                post["number_word"] = is_line_chapter.group(1)
                post["number"] = int(is_line_chapter.group(2))
                all_lines.remove(line)

            if is_line_the_chapter:
                post["cardinal_word"] = is_line_the_chapter.group(1)
                post["cardinal_number"] = is_line_the_chapter.group(2)
                all_lines.remove(line)

    post.content = "".join(all_lines)
    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
