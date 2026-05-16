import csv
import re
from difflib import SequenceMatcher


item_pattern: str = r"(\d+)\. (\w+): (.+)"
choice_pattern: str = r"([abcd])\. (.+)"
answer_pattern: str = r"(\d+) ([abcd])"


def convert_abcd_to_1234(choice: str = ""):
    return


for form in "abc":
    with open(f"./test/ngslt_{form}.csv", mode="w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter="\t")

        # write header
        csvwriter.writerow(
            ["number", "lemma", "question", "1", "2", "3", "4", "answer"]
        )

        with open(f"./test/ngslt_{form}.txt", mode="r") as f:
            lines: list[str] = f.read().splitlines()  # split into lines, not chars

        rows: list[list[str]] = []
        answers: dict[int, int] = {}

        # current item state, carried across iterations
        number: int = -1
        lemma: str = ""
        question: str = ""
        choices: dict[int, str] = {}  # {"a": "...", "b": "...", ...}

        for line in lines:
            is_item = re.match(item_pattern, line)
            is_choice = re.match(choice_pattern, line)
            is_answer = re.match(answer_pattern, line)

            if is_item:  # 1. case: This is a good case.
                if number > -1:  # save previous item before starting a new one
                    rows.append(
                        [
                            str(number),
                            lemma,
                            question,
                            *(choices[i] for i in range(1, 4 + 1)),
                        ]
                    )

                number = int(is_item.group(1)) + 1
                lemma: str = is_item.group(2)
                question: str = is_item.group(3)

                # bold the target word
                for i, word in enumerate(split := question.split()):
                    if SequenceMatcher(a=lemma, b=word.lower()).ratio() > 0.7:
                        split[i] = f"*{word}*"
                        split[i] = re.sub(r"([?.!,])\*", r"*\1", split[i])  # .* → *.

                question = " ".join(split)

            if is_choice:  # a. place to study
                choices["abcd".index(is_choice.group(1)) + 1] = is_choice.group(2)

            if is_answer:  # 65 c
                answers[int(is_answer.group(1)) - 1] = (
                    "abcd".index(is_answer.group(2)) + 1
                )

        if number > -1:  # save the last item
            rows.append(
                [
                    str(number),
                    lemma,
                    question,
                    *(choices[i] for i in range(1, 4 + 1)),
                ]
            )

        # MANUAL FIX
        fix = {  # Python doesn't split the periods
            "steal": "stolen.",
            "occupy": "occupied.",
            "freeze": "frozen.",
            "try": "trying.",
            "catch": "caught",
            "snap": "snapped.",
        }

        for row in rows:  # 0: number, 1: lemma, 2: question
            number: int = int(row[0])
            lemma: str = row[1]
            question: str = row[2]

            if "*" not in question:
                for i, word in enumerate(split := question.split()):
                    if split[i] == fix[lemma]:
                        split[i] = f"*{fix[lemma]}*"
                        split[i] = re.sub(r"([?.!,])\*", r"*\1", split[i])  # .* →
                row[2] = " ".join(split)

            if question.count("*") > 2:
                row[2] = row[2].replace("*it*", "it")

        # write rows, attaching the answer from the answer key
        for i, row in enumerate(rows, start=1):
            csvwriter.writerow(row + [answers[i-1]])
