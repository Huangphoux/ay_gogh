import os
from tqdm import tqdm
from langdetect import detect

# from langdetect import DetectorFactory
# DetectorFactory.seed = 0

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")

# Initialize global exclude_char list
exclude_char = []


# Read non-English characters from non_english.txt
def load_exclude_chars():
    global exclude_char
    non_english_file = os.path.join(os.path.dirname(__file__), "non_english.txt")
    try:
        with open(non_english_file, mode="r", encoding="utf-8") as f:
            exclude_char = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Warning: non_english.txt not found")


def isLineSkippable(line):
    isSkippable = False

    for char in exclude_char:
        if char in line:
            isSkippable = True
            break

    return isSkippable


def detect_non_english(input_file):
    load_exclude_chars()

    with open(input_file, mode="r", encoding="utf-8") as f:
        all_lines = f.readlines()
        content = all_lines

        # Skip empty files
        if not content:
            return

        longest_length = len(max(content, key=len))

    # Then write the processed content
    with open(input_file, mode="w", encoding="utf-8") as f:
        for line in content:
            if isLineSkippable(line):
                continue

            try:
                if len(line.strip()) <= longest_length // 3:
                    f.write(line)
                    continue

                if detect(line.lower().strip()) == "en":
                    f.write(line)
                    continue
                else:
                    f.write("WEIRD\t\t" + line)
            except:
                f.write("WEIRD\t\t" + line)


if __name__ == "__main__":
    # Load the non-English characters
    load_exclude_chars()
    print(exclude_char)
    

    for root, _, files in os.walk(save_path):
        for filename in tqdm(files):
            file_path = os.path.join(root, filename)
            try:
                detect_non_english(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
