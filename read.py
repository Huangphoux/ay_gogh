from test import get_last_test
from apswutils.db import NotFoundError
from starhtml import *
from shared import db, relay, template
import mistletoe
from math import ceil
from mistletoe.html_renderer import HTMLRenderer
import re
import simplemma
from popup import popup_view

rt: APIRouter = APIRouter("/read")


def get_ease(score: int, ngsl: float):
    ease = score * ngsl

    if ease > 90:
        return "easy"

    if 80 <= ease <= 90:
        return "medium"

    if ease < 80:  # why did i write 80 < ease :'(
        return "hard"


@rt.get("/")
def read(auth, p: int = 0, all: int = 0):
    if p not in (0, 1, 2, 3, 4, 5) or all not in (0, 1):
        return Redirect("/read")

    if all:
        chap = list(db.app.query("SELECT number, title, ngsl FROM chapter"))
    else:
        chap = db.app.query(
            "SELECT number, title, ngsl FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
        )

    user_chap = list(db.get(auth).query("SELECT number, done FROM chapter"))

    if user_chap:
        completed_numbers = {uc["number"] for uc in user_chap} # LLM comes up with this
        for c in chap:
            if c["number"] in completed_numbers:
                c["done"] = 1

    last_test = get_last_test(auth)
    result = last_test["result"] if last_test else None
    progress = last_test["progress"] if last_test else None

    main = Main(
        H1(id="main-heading")(
            f"Read, {p * 10 + 1} to {(p + 1) * 10}" if not all else "Read All",
        ),
        # pagination
        Div(style="display: flex; gap: 1rem; align-items: center; height: 1.5rem")(
            A(href=f"/read/?p={p - 1}")("Previous")
            if p > 0
            else Span(style="color: var(--border)")("Previous"),
            *(
                A(href=f"/read/?p={i}")(i)
                if i != p
                else Span(
                    style="font-style: italic; font-weight: bold; font-size: 3rem"
                )(i)
                for i in range(0, 6)
            ),
            A(href=f"/read/?p={p + 1}")("Next")
            if p < 5
            else Span(style="color: var(--border)")("Next"),
        )
        if not all
        else None,
        Ul(
            *(
                Li(style="display: flex; justify-content: space-between;")(
                    A(
                        href=f"/read/{c['number']}",
                        style="color: var(--border)"
                        if "done" in c and c["done"] == 1
                        else None,
                    )(
                        "(DONE)"
                        if "done" in c and c["done"] == 1
                        else f"Chapter {c['number']}: {c['title']}"
                    ),
                    A(style="display: grid;  place-items: center;")(
                        _class=(ease := get_ease(result, c["ngsl"])),
                        href=f"/read/{c['number']}/ease",
                        title=f"You know {result * c['ngsl']:.2f}% of the words in chapter {c['number']}.",
                    )(ease.title())
                    if result
                    and progress == 100
                    and not ("done" in c and c["done"] == 1)
                    else None,
                )
                for c in chap
            ),
        ),
        A(href="/read/?all=1")("Show all")
        if not all
        else A(href="/read/?all=0")("Show less"),
    )

    return template(
        f"Read, {p * 10 + 1} to {(p + 1) * 10}" if not all else "Read All", main, auth
    )


@rt.get("/{num:int}/ease")
async def ease(auth, num: int):
    if num not in range(1, 60 + 1):
        return Redirect("/read")

    chap = list(db.app.query("SELECT ngsl FROM chapter WHERE number = ? ", (num,)))[0]

    last_test = get_last_test(auth)

    if last_test:
        if last_test["progress"] != 100:
            return Redirect(f"/read/{num}")

        score = last_test["result"]
        ease = get_ease(score, chap["ngsl"])
    else:
        return Redirect(f"/read/{num}")

    main = Main(
        H1(id="main-heading")(f"Chapter {num}: Reading Ease"),
        Section(
            Table(
                Thead(Tr(Th("Explanation"), Th("Percentage"))),
                Tbody(
                    Tr(Td(f"NGSL words in chapter {num}"), Td(f"{chap['ngsl']:.2%}")),
                    Tr(Td(f"NGSL words that you know"), Td(f"{score}%")),
                    Tr(
                        Td(f"NGSL words that you know in chapter {num}"),
                        Td(_class=ease)(f"{score * chap['ngsl']:.2f}%"),
                    ),
                ),
            ),
            P(
                "This chapter is deemed of ",
                Span(_class=ease)(ease.title()),
                " difficulty for you.",
            ),
            A(href=f"/read/{num}", _class="button")("Let's read!"),
        ),
        Section(
            P(
                "The table below refers to how difficult a chapter is \
                if you know a centain percentage of words in a chapter."
            ),
            P(
                "This information is taken from ",
                A(href="https://www.newgeneralservicelist.com/coverage")(
                    "The Importance of Coverage in Vocabulary Learning"
                ),
                " by the New General Service List Project.",
            ),
            Table(
                Thead(
                    Tr(
                        Th("Percentage"),
                        Th("Difficulty"),
                    )
                ),
                Tbody(
                    Tr(Td(f"≥ 90%"), Td(_class="easy")("Easy")),
                    Tr(Td(f"80% < x < 90%"), Td(_class="medium")("Medium")),
                    Tr(Td(f"≤ 80%"), Td(_class="hard")("Hard")),
                ),
            ),
        ),
    )

    return template(f"Read, Chapter {num}'s reading ease", main, auth)


@rt.get("/{num:int}")
def chapter(auth, num: int, word: str = ""):
    if num not in range(1, 60 + 1):
        return Redirect("/read")

    return template(
        f"Read, Chapter {num}", auth=auth, main=chapter_main(auth, num, word)
    )


@rt.get("/{num:int}/cqrs")
@sse
async def cqrs(req, auth, num: int):
    async for _, data in relay.subscribe(f"read.{auth}.{num}"):
        yield elements(
            chapter_main(auth, num, word=data),
            selector="main",
            use_view_transition=True,
        )


class MyRenderer(HTMLRenderer):
    def render_block_code(self, token):  # code block → aside
        code = self.escape_html_text(token.children[0].content)
        return Safe(Pre(_class="aside")(code))


def highlight_word(content: str, word: str, due_class: str) -> str:
    code_block: bool = False

    for i, line in enumerate(split := (content.splitlines())):
        if line == "```":
            code_block = not code_block
        if code_block:
            continue

        tokens = simplemma.simple_tokenizer(line)
        lemmas = simplemma.text_lemmatizer(line, lang="en")

        for j, lemma in enumerate(lemmas):
            if word == lemma:
                split[i] = re.sub(
                    r"\b%s\b" % tokens[j],
                    Safe(Span(_class=due_class)(tokens[j])),
                    split[i],  # why can't i use `line` here?
                )

    return "\n".join(split)


def chapter_main(auth, num: int, word: str = ""):
    word = simplemma.lemmatize(word, lang="en") if word else ""

    # execute for INSERT, query for SELECT
    # this one is app
    chap = list(db.app.query("SELECT * FROM chapter WHERE number = ? ", (num,)))[0]

    try:  # this one is user's "done"
        done = db.get(auth).item("SELECT done FROM chapter WHERE number = ? ", (num,))
    except NotFoundError:
        done = 0

    try:
        cards = list(
            db.get(auth).query(
                """
                SELECT
                    front, back, due, last_review, retire,
                    CASE WHEN datetime() > due THEN 1 ELSE 0 END AS is_due,
                           -- datetime now is after due
                    CASE WHEN (last_review IS NULL AND julianday('now') - julianday(due) < 1) THEN 0 ELSE 1 END AS is_new_day
                           --  no last_review       &   it has been 24 hours
                FROM deck
                """
            ),
        )
    except IndexError:
        cards = None

    if cards:
        for c in cards:  # highlight mined words
            due_class = "n0t-du3"

            if not c["is_new_day"]:
                due_class = "n0t-y3t"
            elif c["is_due"]:
                due_class = "du3"

            if c["retire"]:
                due_class = "r3t1r3"

            chap["content"] = highlight_word(chap["content"], c["front"], due_class)

    return Main(
        data_init=get(url=f"/read/{num}/cqrs"),
        data_on_selectionchange=(
            "$word = document.getSelection().toString().trim()",
            dict(document=True),
        ),
    )(
        popup_view(auth, num, word),
        Section(
            style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;"
        )(
            P(f"Chapter {chap['number_word']} ({num})"),
            P(f"The {chap['cardinal_word']} ({chap['cardinal']}) Chapter"),
        ),
        H1(id="main-heading", style="display:grid; place-items: center")(
            f"{chap['title']}",
            " (DONE)" if done else None,
        ),
        Section(
            data_on_pointerup=f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};",
        )(
            Safe(
                mistletoe.markdown(chap["content"], MyRenderer),  # text section
            ),
        ),
        Section(
            H2("Due words"),
            Ul(
                data_on_pointerup=(
                    f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};"
                )
            )(
                *(
                    Li(c["front"])
                    for c in cards
                    if c["is_due"] and c["is_new_day"] and not c["retire"]
                )
            ),
        )
        if cards
        and [1 for c in cards if c["is_due"] and c["is_new_day"] and not c["retire"]]
        else None,
        Section(style="display: grid; place-items: center")(
            Button(data_on_click=patch(f"/read/{num}"))("Mark Complete")
            if not done
            else (
                Button(data_on_click=delete(f"/read/{num}"))("Undo Complete"),
                P(_class="notice")("You have marked this chapter as Complete."),
                A(href=f"/read/?p={ceil(num / 10) - 1}")("Back to List"),
            )
        ),
    )


@rt.patch("/{num:int}")
def done(auth, num: int):
    db.get(auth).execute(
        "INSERT OR REPLACE INTO chapter (number, done) VALUES (?, ?)", (num, 1)
    )
    relay.publish(f"read.{auth}.{num}", "")


@rt.delete("/{num:int}")
def undone(auth, num: int):
    db.get(auth).execute("DELETE FROM chapter WHERE number=?", (num,))
    relay.publish(f"read.{auth}.{num}", "")
