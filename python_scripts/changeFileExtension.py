import os
from tqdm import tqdm

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def changeFileExtension(inputFile):
    if inputFile.endswith(".txt"):
        new_file = inputFile.replace(".txt", ".md")

        try:
            os.rename(inputFile, new_file)
        except OSError as e:
            print(f"Error renaming {inputFile}: {str(e)}")


if __name__ == "__main__":
    for root, _, files in os.walk(savePath):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                changeFileExtension(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
