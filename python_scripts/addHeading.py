import os
from tqdm import tqdm


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addHeading(inputFile):
    # First read the content
    with open(inputFile, mode="r", encoding="utf-8") as f:
        allLines = f.readlines()
        first3Lines = allLines[:3]
        content = allLines[3:]

        # Skip empty files
        if not content:
            return

    # Then write the processed content
    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in first3Lines:
            f.write("# " + line)

        for line in content:
            if "WORDS" in line:
                f.write("# Words\n")
                continue

            f.write(line)


if __name__ == "__main__":
    for root, _, files in os.walk(savePath):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                addHeading(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
