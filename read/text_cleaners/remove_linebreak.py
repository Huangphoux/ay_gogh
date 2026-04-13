import os

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")


def remove_linebreak(fname):
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

    with open(fname, mode="w", encoding="utf-8") as f:
        for line in frontmatter:
            f.write(line)

        is_in_codeblock = False

        for index, line in enumerate(content[:]):
            if "```" in line:
                is_in_codeblock = not is_in_codeblock

            if is_in_codeblock:
                content[index] = line.replace("```", "\n```")
                continue
            
            content[index] = line.replace(" \n", " ").replace(" \r", "")

                
        for line in content[:]:
            f.write(line)
