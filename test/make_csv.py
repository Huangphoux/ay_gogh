import csv
import re
from difflib import SequenceMatcher


item_pattern: str = r"(\d+)\. (\w+): (.+)"
choice_pattern: str = r"([abcd])\. (.+)"
answer_pattern: str = r"(\d+) ([abcd])"

for form in "abc":
    with open(f"./test/ngslt_{form}.csv", mode="w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter="\t")

        # write header
        csvwriter.writerow(
            ["number", "lemma", "question", "a", "b", "c", "d", "answer"]
        )

        with open(f"./test/ngslt_{form}.txt", mode="r") as f:
            lines: list[str] = f.read().splitlines()  # split into lines, not chars

        rows: list[list[str]] = []
        answers: dict[int, str] = {}

        # current item state, carried across iterations
        number: int = -1
        lemma: str = ""
        question: str = ""
        choices: dict[str, str] = {}  # {"a": "...", "b": "...", ...}

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
                            choices.get("a", ""),
                            choices.get("b", ""),
                            choices.get("c", ""),
                            choices.get("d", ""),
                        ]
                    )

                number = int(is_item.group(1)) + 1
                lemma: str = is_item.group(2)
                question: str = is_item.group(3)
                choices: dict[str, str] = {}

                # bold the target word
                for i, word in enumerate(question_splited := question.split()):
                    if SequenceMatcher(a=lemma, b=word).ratio() > 0.7:
                        question_splited[i] = f"**{word}**"
                        question_splited[i] = re.sub(
                            r"([?.!,])\*\*", r"**\1", question_splited[i]
                        )

                question = " ".join(question_splited)

            if is_choice:  # a. place to study
                choices[is_choice.group(1)] = is_choice.group(2)

            if is_answer:  # 65 c
                answers[int(is_answer.group(1)) - 1] = is_answer.group(2)

        if number > -1:  # save the last item
            rows.append(
                [
                    str(number),
                    lemma,
                    question,
                    choices.get("a", ""),
                    choices.get("b", ""),
                    choices.get("c", ""),
                    choices.get("d", ""),
                ]
            )

        # write rows, attaching the answer from the answer key
        for row_number, row in enumerate(rows, start=1):
            answer_letter: str = answers.get(row_number - 1, "")
            answer_text: str = (
                row["abcd".index(answer_letter) + 3] if answer_letter else ""
            )  # index of "a" + 3
            csvwriter.writerow(row + [answer_text])
