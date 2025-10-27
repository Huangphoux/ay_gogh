import os
import frontmatter
from textstat.textstat import textstat


savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test")

textstat_funcs = (
    textstat.flesch_reading_ease,
    textstat.flesch_kincaid_grade,
    textstat.smog_index,
    textstat.coleman_liau_index,
    textstat.automated_readability_index,
    textstat.dale_chall_readability_score,
    textstat.difficult_words,
    textstat.linsear_write_formula,
    textstat.gunning_fog,
    textstat.text_standard,
)


def addReadability(inputFile):
    with open(inputFile, mode="r", encoding="utf-8") as f:
        content = f.read()
        post = frontmatter.loads(content)

        for item in textstat_funcs:
            number = item(content.replace("\t", ""))
            
            try:
                number = round(float(number), 2)
            except:
                pass
            
            post[item.__name__] = number

    with open(inputFile, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))
