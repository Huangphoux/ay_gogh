import os
from tqdm import tqdm


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def deleteCodeBlock(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return

    # Process and write back
    with open(inputFile, mode="w", encoding="utf-8") as f:
        i = 0
        while i < len(lines):
            if "```" in lines[i]:
                i += 1  # Skip opening ```

                content = []
                # stop while loop when line[i] has "```"
                while i < len(lines) and "```" not in lines[i]:
                    content.append(lines[i])
                    i += 1

                if len(content) == 1 and "=" not in content[0]:
                    f.write(content[0])
                elif len(content) == 1 and "=" in content[0]:
                    f.write("```\n")
                    f.writelines(content)
                    f.write("```\n")
                else:
                    f.write("```\n")
                    f.writelines(content)
                    f.write("```\n")

                i += 1  # Skip closing ```
            else:
                f.write(lines[i])
                i += 1


if __name__ == "__main__":
    for root, _, files in os.walk(savePath):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                deleteCodeBlock(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
