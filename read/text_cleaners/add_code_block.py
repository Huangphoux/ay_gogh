import os

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def add_code_block(fname):
    # First read the content
    with open(fname, mode="r", encoding="utf-8") as f:
        all_lines = f.readlines()

        # Skip frontmatter (YAML between --- markers)
        frontmatter_end = 0
        if all_lines and all_lines[0].strip() == "---":
            for i in range(1, len(all_lines)):
                if all_lines[i].strip() == "---":
                    frontmatter_end = i + 1
                    break

        frontmatter = all_lines[:frontmatter_end]
        content = all_lines[frontmatter_end:]

        # Skip empty files
        if not content:
            return

        # Length of the longest line
        max_line_length = len(max(content, key=len))

    # Then write the processed content
    with open(fname, mode="w", encoding="utf-8") as f:
        for line in frontmatter:
            f.write(line)

        is_codeblock_open = False

        for line in content:
            if len(line.strip()) < max_line_length / 3:
                if not is_codeblock_open:
                    is_codeblock_open = True
                    f.write("```\n")
            else:
                if is_codeblock_open:
                    is_codeblock_open = False
                    f.write("```\n")

            f.write(line)

        # Close any remaining open code block
        if is_codeblock_open:
            f.write("```\n")
