from apswutils.db import NotFoundError
from starhtml import *
from shared import db, html_header, html_footer, relay
import mistletoe
from math import floor
import requests
import json


# from fasthtml.components → from starhtml.tags
# from starhtml.tags import Chapter_number, Search_Popup, Word, Definition

read_rt: APIRouter = APIRouter("/read")


@read_rt.get("/")
def read(sess, p: int = 0, all: int = 0):
    if p < 0 or p > 5 or all not in (0, 1):
        return Redirect("/")

    chap = list(
        db.app.query("SELECT number, title FROM chapter")
        if all
        else db.app.query(
            "SELECT number, title FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
        )
    )

    user_chap = list(db.get(sess["name"]).query("SELECT number, done FROM chapter"))

    if user_chap:
        for uc in user_chap:
            for c in chap:
                if uc["number"] == c["number"]:
                    c["done"] = 1

    return (
        Title(
            f"Read, {p * 10 + 1} to {(p + 1) * 10}: Ay Gogh"
            if not all
            else "Read All: Ay Gogh"
        ),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1(id="main-heading")(
                    f"Read ({p * 10 + 1} to {(p + 1) * 10})" if not all else "Read All",
                ),
                Div(
                    style="display: flex; gap: 1rem; align-items: center; height: 1.5rem"
                )(
                    A(href=f"/read/?p={p - 1}")("Previous")
                    if not all and p > 0
                    else Span(style="color: var(--border)")("Previous"),
                    *(
                        A(href=f"/read/?p={i}")(i)
                        if i != p
                        else Span(
                            style="font-style: italic; font-weight: bold; font-size: 3rem"
                        )(i)
                        for i in range(0, 6)
                    ),
                    A(
                        href=f"/read/?p={p + 1}",
                    )("Next")
                    if not all and p < 5
                    else Span(style="color: var(--border)")("Next"),
                )
                if not all
                else None,
                Ul(
                    *(
                        Li(
                            A(
                                href=f"/read/{c['number']}",
                                style="color: var(--border)"
                                if "done" in c and c["done"] == 1
                                else None,
                            )(
                                "(DONE)"
                                if "done" in c and c["done"] == 1
                                else f"Chapter {c['number']}: {c['title']}",
                            ),
                        )
                        for c in chap
                    ),
                ),
                A(href="/read/?all=1")("Show all")
                if not all
                else A(href="/read/?all=0")("Show less"),
            ),
            html_footer(sess),
        ),
    )


@read_rt.get("/{num:int}")
def chapter_get(sess, num: int):
    if num not in range(1, 60 + 1):
        return Redirect("/")

    return chapter_view(sess, num)


@read_rt.get("/{num:int}/cqrs")
@sse
async def cqrs(req, sess, num: int):
    async for subject, data in relay.subscribe(f"read.{sess['name']}.{num}"):
        yield elements(chapter_view(sess, num, word=data), use_view_transition=True)


def chapter_view(sess, num: int, word: str = ""):
    # execute for INSERT, query for SELECT
    chap = list(db.app.query("SELECT * FROM chapter WHERE number = ? ", (num,)))[0]

    try:
        done = db.get(sess["name"]).item(
            "SELECT done FROM chapter WHERE number = ? ", (num,)
        )
    except NotFoundError:
        done = 0

    return (
        Title(f"Read, Chapter {num}: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                data_init=(
                    get(url=f"/read/{num}/cqrs"),
                    "; document.addEventListener('selectionchange', () => $word = document.getSelection().toString().trim())",
                ),
            )(
                popup_view(sess, num, word),
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
                    data_on_pointerup=(
                        f"if ($word !== \"\" ) {{ @get('/read/{num}/add') }};"
                    )
                )(  # text section
                    P(
                        Safe(
                            mistletoe.markdown(chap["content"]),
                        ),
                    ),
                ),
                Section(style="display: grid; place-items: center")(
                    Button(
                        data_on_click=post(f"/read/{num}"),
                    )("Mark Complete")
                    if not done
                    else None,
                    P(_class="notice")("You have marked this chapter as Complete.")
                    if done
                    else None,
                    A(href=f"/read/?p={floor(num / 10)}")("Back to List")
                    if done
                    else None,
                ),
            ),
            html_footer(sess),
        ),
    )


@read_rt.post("/{num:int}")
def complete(sess, num: int):
    db.get(sess["name"]).execute(
        "INSERT OR REPLACE INTO chapter (number, done) VALUES (?, ?)", (num, 1)
    )

    relay.publish(f"read.{sess['name']}.{num}", "")


@read_rt.get("/{num:int}/add")
def add(sess, num: int, word: str):
    relay.publish(f"read.{sess['name']}.{num}", word)


@read_rt.get("/{num:int}/close")
def close(sess, num: int):
    relay.publish(f"read.{sess['name']}.{num}", "")


def popup_view(sess, num: int, word: str = ""):
    if not word:
        return None

    try:
        card = list(
            db.get(sess["name"]).query(
                "SELECT front, back FROM deck WHERE front = ? ", (word,)
            ),
        )[0]
    except IndexError:
        card = None

    if not card:
        try:
            fetch = json.loads(
                requests.get(
                    f"https://freedictionaryapi.com/api/v1/entries/en/{word.lower()}"
                ).text
            )["entries"][0]

            definition = [
                s["definition"]
                for s in fetch["senses"]
                if "(obsolete)" not in s["definition"]
            ]

        except IndexError:
            definition = None

    return Form(
        _class="notice modal",
        data_on_submit=(
            post(
                f"/read/{num}/save",
                {"contentType": "form"},
            )
            if not card
            else patch(
                f"/read/{num}/save",
                {"contentType": "form"},
            ),
        ),
    )(
        Label(_for="word")("Word (cannot change)"),
        Input(
            type="text",
            id="word",
            name="word",
            value=card["front"] if card else word,
            minlength="1",
            required=True,
            placeholder="Write the word you want to collect here.",
            readonly=True,
        ),
        Label(_for="definition")("Definition"),
        Textarea(
            id="definition",
            name="definition",
            placeholder="Write your own definitions in here.",
            required=True,
            minlength="1",
            style="resize: none;",
        )(card["back"] if card else None),
        Details(
            Summary("Wiktionary"),
            Ul(
                style="max-height: 20vh; overflow: auto",
                data_on_pointerup=(
                    f"if ($word !== \"\" ) {{ @get('/read/{num}/add') }};"
                ),
            )(
                *(Li(d) for d in definition),
            ),
        )
        if not card and definition
        else None,
        Div(style="display: flex; gap: 1rem;")(
            Button(type="reset", data_on_click=get(f"/read/{num}/close"))("Close"),
            Button("Save"),
        ),
    )


@read_rt.post("/{num:int}/save")
async def save(sess, num: int, word: str, definition: str):
    if word and definition:
        db.get(sess["name"]).execute(
            "INSERT OR REPLACE INTO deck (front, back) VALUES (?, ?)",
            (word, definition),
        )

        relay.publish(f"read.{sess['name']}.{num}", "")


@read_rt.patch("/{num:int}/save")
async def save(sess, num: int, word: str, definition: str):
    if word and definition:
        db.get(sess["name"]).execute(
            "INSERT OR REPLACE INTO deck (front, back) VALUES (?, ?)",
            (word, definition),
        )

        relay.publish(f"read.{sess['name']}.{num}", "")
