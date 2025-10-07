import re
import os
from langdetect import detect

from langdetect import DetectorFactory
DetectorFactory.seed = 0

# Dòng đó có nguyên cụm "Chapter"
# sau đó là các kí tự gì ko quan tâm
# sau đó capture group là số nằm trong ()

pattern = r"Chapter.+\((\d+)\)"
save_path = r'D:\Projects\ay_gogh\test'

""" 
- Detect nếu dòng đó chứa "Chapter" và (n)
- Lưu dòng đó và các dòng ở dưới nó cho đến dòng chứa "Chapter" và (n+1)
"""

def split_chapters(input_file):
    curr_chap = 0
    
    with open(input_file, mode="r", encoding="utf-8") as f:
        content = f.readlines()
        
    for line in content:
        match = re.match(pattern, line)
        
        # If this is a chapter heading
        if match:
            if match.group(1) != curr_chap:
                curr_chap = match.group(1)

        output_file = os.path.join(save_path, f"{curr_chap}.md")
        with open(output_file, "a", encoding="utf-8") as out:
            out.writelines(line)

if __name__ == "__main__":
    split_chapters("full.txt")