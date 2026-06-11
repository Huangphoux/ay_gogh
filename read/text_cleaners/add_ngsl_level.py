import os
import spacy
import frontmatter
import csv
from math import ceil

save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")
ngsl_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "ngsl", "NGSL_1.2_stats_modified.csv"
)
lemma_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ngsl",
    "NGSL_1.2_lemmatized_for_teaching_modified.csv",
)
skip_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skip_list.txt")

nlp = spacy.load("en_core_web_sm")
# uv run spacy download en_core_web_sm
words = set(nlp.vocab.strings)

with open(ngsl_path, mode="r", encoding="utf-8") as f:
    # ValueError, I/O operation on closed file
    # OH MY GOD ?!
    # the solution was simply to make the csv.reader a list to avoid file closure???
    # Claude Haiku pointed this out for me, I am so ashamed for resorting to LLM

    ngsl: dict[str, str] = {}

    for row in list(csv.reader(f)):  # ["the","1","87.85","60910"]
        ngsl[row[0]] = row[1]

with open(lemma_path, mode="r", encoding="utf-8") as f:
    form_to_lemma: dict[str, str] = {}

    for row in list(csv.reader(f)):  # ["abandon","abandons","abandoned","abandoning"]
        for item in row:
            form_to_lemma[item] = row[0]

with open(skip_path, mode="r", encoding="utf-8") as f:
    skip = {line.strip() for line in f}


def add_ngsl_level(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.readlines()
        max_line_length = len(max(content, key=len))

        # remove code block: line length < max line length / 5
        content = " ".join(
            [line for line in content if len(line.strip()) > max_line_length / 5]
        )

        lemma: set[str] = {""}  # unique lemma only
        lemma.remove("")

        for token in nlp(content):
            if token.is_alpha:
                if (
                    token.lemma_ in skip
                    or token.lemma_.istitle()
                    or token.lemma_ not in words
                ):
                    # words doesn't consider outdated vocab tho
                    continue

                if (
                    token.lemma_ in form_to_lemma
                    and token.lemma_ != form_to_lemma[token.lemma_]
                ):
                    # print(token.text, token.lemma_, form_to_lemma[token.lemma_])
                    # not form_to_lemma[token.text
                    lemma.add(form_to_lemma[token.lemma_])
                else:  # i forgot this else, it will add "her" regardless
                    lemma.add(token.lemma_)

        lv: list[int] = [0, 0, 0, 0, 0, 0]  # lv[0]: not ngsl

        for l in lemma:
            if l in ngsl:
                lv[ceil(int(ngsl[l]) / 562)] += 1
            else:
                lv[0] += 1

        sum = len(lemma)

        # print(f"{1 - (lv[0] / sum):.2%}")
        # print([f"{lv[i] / sum:.2%}" for i in range(0, 5 + 1)])
        # đa số lý do lv0 nhiều là do còn dư âm của phiên âm IPA

    with open(fname, mode="r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        # f being busy being read by f.readlines() so has to make a new open()

        # for i in range(0, 5 + 1):
            # post[f"lv{i}"] = lv[i] / sum

        post["ngsl"] = (lv[1] + lv[2] + lv[3] + lv[4] + lv[5]) / sum

    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
