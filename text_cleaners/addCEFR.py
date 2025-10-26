import os
import readtime
import frontmatter


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def get_word_level_count_statistic(
    level_tokens: list[tuple[str, str, bool, float, int, int]],
) -> list[int]:
    difficulty_levels_count = [0] * 6
    for token in level_tokens:
        level = token[3]
        if not level:
            continue

        level_round = round(level)
        difficulty_levels_count[level_round - 1] += 1

    return difficulty_levels_count


def addCEFR(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        read_time = readtime.of_markdown(post.content).text
        post["read-time"] = read_time

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
