import csv
import re

item_pattern: str = r"(\d+)\. (\w+): (.+)"
choice_pattern: str = r"([abcd])\. (.+)"
answer_pattern: str = r"(\d+) ([abcd])"


def get_level(num: str) -> int:
    if int(num) in range(1, 21):  # range(i, j): [i, j)
        return 1
    if int(num) in range(21, 41):
        return 2
    if int(num) in range(41, 61):
        return 3
    if int(num) in range(61, 81):
        return 4
    if int(num) in range(81, 102):
        return 5
    return 0


with open("./test/ngslt.csv", mode="w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="\t")

    # write header
    csvwriter.writerow(["Lemma", "Level", "Question", "A", "B", "C", "D", "Answer"])

    for form in ("a", "b", "c"):
        with open(f"./test/ngslt_{form}.txt", mode="r") as f:
            lines: list[str] = f.read().splitlines()  # split into lines, not chars

        rows: list[list[str]] = []
        answers: dict[int, str] = {}

        # current item state, carried across iterations
        number: int = 0
        level: int = 0
        lemma: str = ""
        question: str = ""
        choices: dict[str, str] = {}  # {"a": "...", "b": "...", ...}

        for line in lines:
            is_item = re.match(item_pattern, line)
            is_choice = re.match(choice_pattern, line)
            is_answer = re.match(answer_pattern, line)

            if is_item:  # 1. case: This is a good case.
                if number > 0:  # save previous item before starting a new one
                    rows.append(
                        [
                            lemma,
                            str(level),
                            question,
                            choices.get("a", ""),
                            choices.get("b", ""),
                            choices.get("c", ""),
                            choices.get("d", ""),
                        ]
                    )

                number = int(is_item.group(1))
                level: int = get_level(is_item.group(1))
                lemma: str = is_item.group(2)
                question: str = is_item.group(3)
                choices: dict[str, str] = {}

            if is_choice:  # a. place to study
                choices[is_choice.group(1)] = is_choice.group(2)

            if is_answer:  # 65 c
                answers[int(is_answer.group(1)) - 1] = is_answer.group(2)

        if number > 0:  # save the last item
            rows.append(
                [
                    lemma,
                    str(level),
                    question,
                    choices.get("a", ""),
                    choices.get("b", ""),
                    choices.get("c", ""),
                    choices.get("d", ""),
                ]
            )

        # write rows, attaching the answer from the answer key
        for row_number, row in enumerate(rows, start=1):
            answer_letter: str = answers.get(row_number, "")
            answer_text: str = (
                row["abcd".index(answer_letter) + 3] if answer_letter else ""
            )  # index of "a" + 3
            csvwriter.writerow(row + [answer_text])
