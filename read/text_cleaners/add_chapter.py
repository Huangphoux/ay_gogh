import os
import re
import frontmatter


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")
chapter_regex = r"Chapter (.+) \((\d+)\)"
the_chapter_regex = r"The (.+) \((\d+.+)\).+Chapter"


def add_chapter(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)
        all_lines = content.splitlines(keepends=True)

        for line in all_lines[:]:
            is_line_chapter = re.match(chapter_regex, line)
            is_line_the_chapter = re.match(the_chapter_regex, line)

            if is_line_chapter:
                number_word = is_line_chapter.group(1)
                number = int(is_line_chapter.group(2))

                post["number_word"] = number_word
                post["number"] = number

            if is_line_the_chapter:
                cardinal_word = is_line_the_chapter.group(1)
                cardinal_number = is_line_the_chapter.group(2)

                post["cardinal_word"] = cardinal_word
                post["cardinal_number"] = cardinal_number

    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
