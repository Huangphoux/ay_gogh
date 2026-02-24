import os


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")


def delete_code_block(fname):
    """

    Check the content between the code blocks.

    If it's only has one line, then don't write the code blocks.
    """

    with open(fname, mode="r", encoding="utf-8") as f:
        lines = f.readlines()

        if not lines:
            return

    # Process and write back

    with open(fname, mode="w", encoding="utf-8") as f:
        i = 0

        while i < len(lines):
            if "```" in lines[i]:
                i += 1  # Skip opening ```

                content = []

                # stop when line has "```"

                while i < len(lines) and "```" not in lines[i]:
                    content.append(lines[i])

                    i += 1

                skip_empty = [x for x in content if x]

                if len(skip_empty) == 1:
                    f.writelines(skip_empty)

                else:
                    f.write("```\n")
                    f.writelines(skip_empty)
                    f.write("```\n")

                i += 1  # Skip closing ```

            else:
                f.write(lines[i])

                i += 1
