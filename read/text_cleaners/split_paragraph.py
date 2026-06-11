import os
import frontmatter
import spacy

nlp = spacy.load("en_core_web_sm")


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")


def split_paragraph(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        post = frontmatter.loads(f.read())
        
        with nlp.select_pipes(enable=['tok2vec', "parser", "senter"]):
          doc = nlp(post.content)
          
        sentences = [str(sent).strip() for sent in doc.sents]
        
        post.content = "\n\n".join(sentences)

    with open(fname, mode="wb") as f:
        f.write(frontmatter.dumps(post).encode("utf-8"))