from load_env import is_debug
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
        chap = db.app.query("SELECT number, title, ngsl FROM chapter")
    else:
        chap = db.app.query(
            "SELECT number, title, ngsl FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
        )

    chap = list(chap)

    chap_done = list(db.get(auth).query("SELECT number, done FROM chapter"))

    completed_numbers = {uc["number"] for uc in chap_done}  # LLM comes up with this
    for c in chap:
        c["done"] = c["number"] in completed_numbers

    last_test = get_last_test(auth)
    result = last_test["result"] if last_test else None
    progress = last_test["progress"] if last_test else None

    if not all:
        h1 = H1(
            id="main-heading",
            style=f"view-transition-name: read",
        )(f"Read, {p * 10 + 1} to {(p + 1) * 10}")

        pagination = Div(
            style="display: flex; gap: 1rem; align-items: center; height: 1.5rem"
        )(
            # Previous
            A(href=f"/read/?p={p - 1}")("Previous")
            if p > 0
            else Span(style="color: var(--border)")("Previous"),
            # Page numbers
            *(
                A(href=f"/read/?p={i}")(i)
                if i != p
                else Span(
                    style="font-style: italic; font-weight: bold; font-size: 3rem"
                )(i)
                for i in range(0, 6)
            ),
            # Next
            A(href=f"/read/?p={p + 1}")("Next")
            if p < 5
            else Span(style="color: var(--border)")("Next"),
        )

        show_all = A(href="/read/?all=1")("Show all")

    else:
        h1 = H1(
            id="main-heading",
            style=f"view-transition-name: read",
        )(f"Read All")
        pagination = None
        show_all = A(href="/read/?all=0")("Show less")

    chapters = Ul(style="padding: 0;")(
        *(
            Li(style="display: flex; justify-content: space-between;")(
                # Chapter {number}: {title}
                Span(
                    Span(style=f"view-transition-name: num{c['number']}")(
                        f"Chapter {c['number']:02}: "
                    ),
                    A(
                        href=f"/read/{c['number']}",
                        style=f"view-transition-name: chap{c['number']}",
                    )(f"{c['title']}")
                    if not c["done"]
                    else A(
                        href=f"/read/{c['number']}",
                        style=f"color: var(--border); view-transition-name: done{c['number']}",
                    )("(DONE)"),
                ),
                # Reading ease difficulty: Easy, Medium, Hard
                A(
                    style=f"display: grid; place-items: center; view-transition-name: ease{c['number']};"
                )(
                    _class=(ease := get_ease(result, c["ngsl"])),
                    href=f"/read/{c['number']}/ease",
                    title=f"You know {result * c['ngsl']:.2f}% of the words in chapter {c['number']}.",
                )(ease.title())
                if result is not None and progress == 100 and not c["done"]
                else None,
            )
            for c in chap
        ),
    )

    main = Main(h1, pagination, chapters, show_all)

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

    h1 = H1(id="main-heading", style=f"view-transition-name: num{num}")(
        f"Chapter {num}: ",
        Span(_class=ease, style=f"view-transition-name: ease{num}")(ease.title()),
    )

    judgement = Section(
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
    )

    reference = Section(
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
            Thead(Tr(Th("Percentage"), Th("Difficulty"))),
            Tbody(
                Tr(Td(f"≥ 90%"), Td(_class="easy")("Easy")),
                Tr(Td(f"80% < x < 90%"), Td(_class="medium")("Medium")),
                Tr(Td(f"≤ 80%"), Td(_class="hard")("Hard")),
            ),
        ),
    )

    main = Main(h1, judgement, reference)

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
            chapter_main(auth, num, word=data["word"], bypass=data["bypass"]),
            selector="main",
            use_view_transition=True,
        )


def mark_word(num: int, content: str, card: dict) -> str:
    showpopup = js(
        f"if ($word !== \"\" ) {{ @get('/read/{num}/open');\
        document.querySelector('#popup').showPopover(); }}; $word = ''"
    )

    click_showpopup = js(f"$word = evt.target.textContent; {showpopup}")

    code_block: bool = False

    for i, line in enumerate(split := (content.splitlines())):
        if line == "```":
            code_block = not code_block
        if code_block:
            continue

        tokens = simplemma.simple_tokenizer(line)
        lemmas = simplemma.text_lemmatizer(line, lang="en")
        marked = []  # pass token if already marked

        for j, lemma in enumerate(lemmas):
            if card["front"] == lemma and tokens[j] not in marked:
                split[i] = re.sub(
                    r"\b%s\b" % tokens[j],
                    Safe(
                        Span(
                            data_is_retired=card["is_retired"],
                            data_is_new_day=card["is_new_day"],
                            data_is_due=card["is_due"],
                            data_attr_style=f"!$show_mark && 'background: initial; text-decoration: underline;'",
                            data_on_pointerup=(click_showpopup, dict(stop=True)),
                            data_indicator="searching",
                        )(tokens[j])
                    ),
                    split[i],  # why can't i use `line` here?
                )

                marked.append(tokens[j])

    return "\n".join(split)


class MyRenderer(HTMLRenderer):
    def render_block_code(self, token):  # code block → aside
        code = self.escape_html_text(token.children[0].content)
        return Safe(Pre(_class="aside", data_show="$show_aside")(code))


def chapter_main(auth, num: int, word: str = "", bypass: int = 0):
    word = simplemma.lemmatize(word, lang="en") if word else ""

    # execute for INSERT, query for SELECT
    # this one is app
    chap = list(db.app.query("SELECT * FROM chapter WHERE number = ? ", (num,)))[0]

    try:  # this one is user's "done"
        done = db.get(auth).item("SELECT done FROM chapter WHERE number = ? ", (num,))
    except NotFoundError:
        done = 0

    try:
        cards = list(  # this one find all cards
            db.get(auth).query(
                """
    SELECT
        front, back, due, last_review, is_retired,
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
        for card in cards:  # mark mined words
            chap["content"] = mark_word(num, chap["content"], card)

    show_aside = db.get(auth).item(
        "SELECT value FROM settings WHERE setting = 'show_aside'"
    )
    show_mark = db.get(auth).item(
        "SELECT value FROM settings WHERE setting = 'show_mark'"
    )

    toggles = Details(data_ignore_morph=True)(
        Summary("Toggles for changing visibility"),
        Ul(
            style="list-style-type: none; width: 100%",
            data_signals=dict(show_mark=int(show_mark), show_aside=int(show_aside)),
        )(
            Li(
                style="display: flex;",
                data_on_change=patch(f"/read/{num}/save_toggles"),
            )(
                Input(
                    type="checkbox",
                    id="show_mark",
                    name="show_mark",
                    data_bind="show_mark",
                ),
                Label(_for="show_mark", style=" flex-shrink: 0; padding-left: 0.5rem")(
                    "Show colorful highlights"
                ),
            ),
            Li(
                style="display: flex;",
                data_on_change=patch(f"/read/{num}/save_toggles"),
            )(
                Input(
                    type="checkbox",
                    id="show_aside",
                    name="show_aside",
                    data_bind="show_aside",
                ),
                Label(_for="show_aside", style=" flex-shrink: 0; padding-left: 0.5rem")(
                    "Show marginal explanations"
                ),
            ),
        ),
    )

    cardinal = Section(_class="cardinal", style="padding: 0; margin: 0;")(
        P(style=f"view-transition-name: num{num}")(
            f"Chapter {chap['number_word']} ({num})"
        ),
        P(f"The {chap['cardinal_word']} ({chap['cardinal']}) Chapter"),
    )

    h1 = H1(
        id="main-heading",
        style=f"display:grid; place-items: center; text-align: center; view-transition-name: chap{num}",
    )(
        f"{chap['title']}",
        Span(style=f"view-transition-name: done{num}")(" (DONE)") if done else None,
    )

    showpopup = js(
        f"if ($word !== \"\" ) {{ @get('/read/{num}/open');\
        document.querySelector('#popup').showPopover(); }};"
    )

    content = Section(data_on_pointerup=showpopup, data_indicator="searching")(
        Safe(
            mistletoe.markdown(chap["content"], MyRenderer),  # text section
        ),
    )

    due_cards = (
        [c for c in cards if c["is_due"] and c["is_new_day"] and not c["is_retired"]]
        if cards
        else None
    )

    retired_cards = [c for c in cards if c["is_retired"]] if cards else None

    click_showpopup = js(f"$word = evt.target.textContent; {showpopup} $word = '';")

    before_complete = (
        Section(
            H2("Due words"),
            Ul(
                *(
                    Li(
                        style="user-select: none; cursor: pointer;",
                        data_on_click=click_showpopup,
                    )(c["front"])
                    for c in due_cards
                )
            ),
        )
        if due_cards
        else None,
        Section(
            H2("Retired words"),
            Ul(
                *(
                    Li(
                        style="user-select: none; cursor: pointer;",
                        data_on_click=click_showpopup,
                    )(c["front"])
                    for c in retired_cards
                )
            ),
        )
        if retired_cards
        else None,
    )

    mark_complete = Section(style="display: grid; place-items: center")(
        Button(data_on_click=(patch(f"/read/{num}"), ";confetti();"))("Mark Complete")
        if not done
        else (
            Button(data_on_click=delete(f"/read/{num}"), _class="outline")(
                "Undo Complete"
            ),
            P(_class="notice")("You have marked this chapter as Complete."),
            A(href=f"/read/?p={ceil(num / 10) - 1}")("Back to List"),
        )
    )

    debug_signals = (
        Details(data_ignore_morph=True)(
            Summary("Panel for debugging signals"),
            Pre(data_json_signals=True),
        )
        if is_debug
        else None
    )

    popup_btn = Button(
        _class="outline",
        style="width: 100%; position: sticky; top: 0; z-index: 2;",
        data_on_click="document.querySelector('#popup').togglePopover();",
    )("Toggle popup")
    
    confetti_script = (
        Script(
            src="https://cdn.jsdelivr.net/npm/@hiseb/confetti@2.1.0/dist/confetti.min.js"
        ),
    )

    return Main(
        data_init=get(url=f"/read/{num}/cqrs"),
        data_on_selectionchange=(
            js("$word = document.getSelection().toString().trim()"),
            dict(document=True),
        ),
    )(
        confetti_script,
        cardinal,
        h1,
        popup_view(auth, num, word, bypass),
        debug_signals,
        toggles,
        popup_btn,
        content,
        before_complete,
        mark_complete,
    )


def publish(auth, num: int, word: str = "", bypass: int = 0):
    # pointerup→open()→cqrs()→popup_view()
    relay.publish(f"read.{auth}.{num}", dict(word=word, bypass=bypass))


@rt.patch("/{num:int}/save_toggles")
def save_toggles(auth, num: int, show_aside: int, show_mark: int):
    db.get(auth).execute(
        "UPDATE settings SET value=? WHERE setting=?", (show_aside, "show_aside")
    )
    db.get(auth).execute(
        "UPDATE settings SET value=? WHERE setting=?", (show_mark, "show_mark")
    )
    publish(auth, num)


@rt.patch("/{num:int}")
def done(auth, num: int):
    db.get(auth).execute(
        "INSERT INTO chapter (number, done) VALUES (?, CURRENT_TIMESTAMP)", (num,)
    )
    publish(auth, num)


@rt.delete("/{num:int}")
def undone(auth, num: int):
    db.get(auth).execute("DELETE FROM chapter WHERE number=?", (num,))
    publish(auth, num)
