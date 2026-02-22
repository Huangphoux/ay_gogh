import os
import frontmatter
from textstat.textstat import textstat


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")

textstat_funcs = (
    # textstat.flesch_reading_ease,
    # textstat.flesch_kincaid_grade,  # grade level
    # textstat.smog_index,  # grade level
    # textstat.coleman_liau_index,  # grade level
    # textstat.automated_readability_index,  # grade level
    # textstat.dale_chall_readability_score,  # grade level
    # textstat.difficult_words,
    # textstat.linsear_write_formula,  # grade level
    # textstat.gunning_fog,
    textstat.text_standard,  # Readability Consensus based upon all the tests
    # textstat.spache_readability,  # grade level
    # textstat.mcalpine_eflaw,  # Should be ≤ 25
    # textstat.words_per_sentence,
    # textstat.is_easy_word,
    # textstat.is_difficult_word,
)


def add_readability(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)

        for item in textstat_funcs:
            number = item(content)

            try:
                number = round(float(number), 2)
            except:
                pass

            post[item.__name__] = number

    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
