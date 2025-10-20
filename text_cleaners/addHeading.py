import os
from tqdm import tqdm


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addHeading(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in content[:10]:
            f.write("# " + line)
            if line.isupper():
                break

        for line in content[10:]:
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
