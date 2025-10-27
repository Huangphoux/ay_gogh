import os
import frontmatter
import spacy
from cefrpy import CEFRSpaCyAnalyzer, CEFRLevel

ABBREVIATION_MAPPING = {
    "'m": "am",
    "'s": "is",
    "'re": "are",
    "'ve": "have",
    "'d": "had",
    "n't": "not",
    "'ll": "will",
}

# uv run spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")


def get_word_level_count_statistic_unique(
    level_tokens: list[tuple[str, str, bool, float, int, int]],
) -> list[int]:
    processed_word_pos_set = set()
    difficulty_levels_count = [0] * 6
    for token in level_tokens:
        level = token[3]
        if not level:
            continue

        to_check_tuple = (token[0], token[1])

        if to_check_tuple not in processed_word_pos_set:
            level_round = round(token[3])
            difficulty_levels_count[level_round - 1] += 1
            processed_word_pos_set.add(to_check_tuple)

    return difficulty_levels_count


def get_not_found_words(
    level_tokens: list[tuple[str, str, bool, float, int, int]],
) -> set[str]:
    not_found_words = set()
    for token in level_tokens:
        if token[2]:
            continue

        if not token[3]:
            not_found_words.add(token[0])

    return not_found_words

def filter_for_desired_level(
    level_tokens: list[tuple[str, str, bool, float, int, int]],
    min_level: float | int = 1.0,
    max_level: float | int = 6.0,
) -> set[tuple[str, str, bool, float, int, int]]:
    filtered_tokens = set()
    for token in level_tokens:
        level = token[3]

        if level and level >= min_level and level <= max_level:
            filtered_tokens.add(token)

    return filtered_tokens


def addCEFR(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)

        text_analyzer = CEFRSpaCyAnalyzer(abbreviation_mapping=ABBREVIATION_MAPPING)

        doc = nlp(post.content)
        tokens = text_analyzer.analize_doc(doc)
        difficulty_levels_count_unique = get_word_level_count_statistic_unique(tokens)

        for i in range(1, 7):
            post[f"{CEFRLevel(i)}"] = difficulty_levels_count_unique[i - 1]
            
        not_found_words_set = get_not_found_words(tokens)
        not_found_words_list = list(not_found_words_set)
        not_found_words_list.sort()
        
        post["IDK"] = ", ".join(not_found_words_list)
        
    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
