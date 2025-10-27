import os


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def addHeading(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.readlines()

    with open(inputFile, mode="w", encoding="utf-8") as f:
        for line in content:
            if "WORDS" in line:
                f.write("# Words\n")
                continue

            f.write(line)
