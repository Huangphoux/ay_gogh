from apswutils.db import NotFoundError
from starhtml import *
from shared import db, relay, template
import mistletoe
from math import ceil
import requests
import json
from fsrs import Scheduler, Card, Rating
from datetime import datetime, timezone
from mistletoe.html_renderer import HTMLRenderer


read_rt: APIRouter = APIRouter("/read")


def get_ease(score: int, ngsl: float):
    ease = score * ngsl
    # return ease

    if ease > 90:
        return "easy"

    if 80 <= ease <= 90:
        return "medium"

    if ease < 80:  # why did i write 80 < ease :'(
        return "hard"


@read_rt.get("/")
def read(auth, p: int = 0, all: int = 0):
    if p < 0 or p > 5 or all not in (0, 1):
        return Redirect(read)

    chap = list(
        db.app.query("SELECT number, title, ngsl FROM chapter")
        if all
        else db.app.query(
            "SELECT number, title, ngsl FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
        )
    )

    user_chap = list(db.get(auth).query("SELECT number, done FROM chapter"))

    if user_chap:
        for uc in user_chap:
            for c in chap:
                if uc["number"] == c["number"]:
                    c["done"] = 1

    try:
        last_test = list(
            db.get(auth).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        last_test = None

    score = (
        sum(last_test[f"lv{x}"] for x in range(1, 5 + 1))
        if last_test and last_test["progress"] == 100
        else None
    )

    main = Main(
        H1(id="main-heading")(
            f"Read, {p * 10 + 1} to {(p + 1) * 10}" if not all else "Read All",
        ),
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
            A(
                href=f"/read/?p={p + 1}",
            )("Next")
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
                        _class=(ease := get_ease(score, c["ngsl"])),
                        href=f"/read/{c['number']}/ease",
                        title=f"You know {score * c['ngsl']:.2f}% of the words in chapter {c['number']}.",
                    )(ease.title())
                    if score and not ("done" in c and c["done"] == 1)
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
        f"Read, {p * 10 + 1} to {(p + 1) * 10}" if not all else "Read All",
        main,
        auth,
    )


@read_rt.get("/{num:int}/ease")
def ease(auth, num: int):
    chap = list(db.app.query("SELECT ngsl FROM chapter WHERE number = ? ", (num,)))[0]

    try:
        last_test = list(
            db.get(auth).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        last_test = None

    if last_test:
        score = sum(last_test[f"lv{x}"] for x in range(1, 5 + 1))
        ease = get_ease(score, chap["ngsl"])
    else:
        return Redirect(f"/read/{num}")

    main = Main(
        H1(id="main-heading")(f"Chapter {num}: Reading Ease"),
        A(href=f"/read/?p={ceil(num / 10) - 1}")("< Back"),
        Section(
            Table(
                Thead(
                    Tr(
                        Th("Explanation"),
                        Th("Percentage"),
                    )
                ),
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

    return template(
        f"Read, Chapter {num}'s reading ease",
        main,
        auth,
    )


@read_rt.get("/{num:int}")
def chapter(auth, num: int, word: str = ""):
    if num not in range(1, 60 + 1):
        return Redirect(read)

    return template(
        f"Read, Chapter {num}/60", auth=auth, main=chapter_main(auth, num, word)
    )


@read_rt.get("/{num:int}/cqrs")
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
        return f"<aside><pre>{code}</pre></aside>"


def chapter_main(auth, num: int, word: str = ""):
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
                    front, back, due, last_review,
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
        for c in cards:
            if c["front"].lower() in chap["content"].lower():
                for item in (c["front"], c["front"].title()):
                    due_class = "n0t-du3"

                    if not c["is_new_day"]:
                        due_class = "n0t-y3t"
                    elif c["is_due"]:
                        due_class = "du3"

                    chap["content"] = chap["content"].replace(
                        item,
                        Safe(Span(_class=due_class)(item)),
                    )

    return Main(
        data_init=get(url=f"/read/{num}/cqrs"),
        data_on_selectionchange=(
            "$word = document.getSelection().toString().trim()",
            {
                "document": True,
            },
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
            data_on_pointerup=(f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};")
        )(  # text section
            P(
                Safe(
                    mistletoe.markdown(chap["content"], HTMLRenderer),
                ),
            ),
        ),
        Section(
            H2("Due words that you may have missed"),
            P("Deal with these before completing this chapter."),
            Ul(
                data_on_pointerup=(
                    f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};"
                )
            )(*(Li(c["front"]) for c in cards if c["is_due"])),
        )
        if cards and [1 for c in cards if c["is_due"] == 1]
        else None,
        Section(style="display: grid; place-items: center")(
            Button(
                data_on_click=post(f"/read/{num}"),
            )("Mark Complete")
            if not done
            else None,
            P(_class="notice")("You have marked this chapter as Complete.")
            if done
            else None,
            A(href=f"/read/?p={ceil(num / 10) - 1}")("Back to List") if done else None,
        ),
    )


@read_rt.post("/{num:int}")
def complete(auth, num: int):
    db.get(auth).execute("INSERT INTO chapter (number, done) VALUES (?, ?)", (num, 1))
    relay.publish(f"read.{auth}.{num}", "")


### POP UP


@read_rt.get("/{num:int}/open")
def open(auth, num: int, word: str):
    relay.publish(f"read.{auth}.{num}", word)  # pointerup→open()→cqrs()→popup_view()
    return Redirect(f"/read/{num}?word={word}")


@read_rt.get("/{num:int}/close")
def close(auth, num: int):
    relay.publish(f"read.{auth}.{num}", "")
    return Redirect(f"/read/{num}")


def popup_view(auth, num: int, word: str = ""):
    if not word:
        return Noscript(
            Form(
                action=f"/read/{num}/open",
                _class="notice modal",
            )(
                Label(_for="word")(
                    "Write the word you want to search in your memory here."
                ),
                Input(
                    type="text",
                    id="word",
                    name="word",
                    value=word,
                    minlength="1",
                    required=True,
                    placeholder="e.g. hawk tuah",
                    style="width: 100%;",
                ),
                Button("Search"),
            )
        )

    if " " in word:
        return Form(_class="notice modal")(
            P(
                'You can only collect a single word, like "six" or "seven". Spaces are not allowed.'
            ),
            Button(
                data_on_click=(get(f"/read/{num}/close"), {"prevent": True}),
            )("Close"),
        )

    try:
        card = list(
            db.get(auth).query(
                """
                SELECT
                    front, back, due, last_review,
                    CASE WHEN datetime() > due THEN 1 ELSE 0 END AS is_due,
                           -- datetime now is after due
                    CASE WHEN (last_review IS NULL AND julianday('now') - julianday(due) < 1) THEN 0 ELSE 1 END AS is_new_day
                           --  no last_review       &   it has been 24 hours
                FROM deck
                WHERE front = ?
                """,
                (word,),
            ),
        )[0]
    except IndexError:
        card = None

    if not card:
        try:
            fetch = json.loads(
                requests.get(
                    f"https://freedictionaryapi.com/api/v1/entries/en/{word}"
                ).text
            )["entries"][0]

            definition = [
                s["definition"]
                for s in fetch["senses"]
                if "(obsolete)" not in s["definition"]
            ]

        except IndexError:
            definition = None

        return Form(_class="notice modal")(
            Label(_for="word")("Word (cannot modify)"),
            Input(
                type="text",
                id="word",
                name="word",
                value=word,
                minlength="1",
                required=True,
                placeholder="Write the word you want to collect in here.",
                readonly=True,
                style="width: 100%;",
            ),
            Label(_for="definition")("Definition"),
            Textarea(
                id="definition",
                name="definition",
                placeholder="Write your definition in here.",
                required=True,
                minlength="1",
                style="resize: none;",
            ),
            Details(
                Summary("Wiktionary"),
                Ul(
                    style="max-height: 20vh; overflow: auto",
                    data_on_pointerup=(
                        f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};"
                    ),
                )(
                    *(Li(d) for d in definition),
                ),
            )
            if definition
            else None,
            Div(style="display: flex; gap: 1rem;")(
                Button(
                    data_on_click=(get(f"/read/{num}/close"), {"prevent": True}),
                    _class="outline",
                    type="submit",
                    formmethod="get",
                    formaction=f"/read/{num}/close",
                    formnovalidate=True,
                )("Close"),
                Button(
                    data_on_click=(post(f"/read/{num}/save", contentType="form")),
                    type="submit",
                    formmethod="post",
                    formaction=f"/read/{num}/save",
                )("Save"),
            ),
        )

    if not card["is_new_day"]:
        return Form(_class="notice modal")(
            Small(
                "※ ",
                Span(_class="n0t-y3t")("Yellow background"),
                ": the word can't be revealed until tomorrow.",
                Br(),
            ),
            Button(
                data_on_click=(get(f"/read/{num}/close"), {"prevent": True}),
            )("Close"),
        )

    if not card["is_due"]:
        time_delta = datetime.strptime(card["due"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        ) - datetime.now(timezone.utc)

        return Form(_class="notice modal")(
            Small(
                " ※ ",
                Span(_class="n0t-du3")("Green background"),
                ": the word is not due for a review yet.",
            ),
            P(
                f"Next review is in {str(time_delta).split('.')[0]}."
            ),  # take only what is before the point
            Button(
                data_on_click=(get(f"/read/{num}/close"), {"prevent": True}),
            )("Close"),
        )

    # default is >= due
    return Form(_class="notice modal")(
        Small(
            "※ ",
            Span(_class="du3")("Red background"),
            ": the word is due for a review.",
        ),
        Label(_for="word")("Word"),
        Input(
            type="text",
            id="word",
            name="word",
            value=card["front"],
            minlength="1",
            required=True,
            placeholder="Write the word you want to collect here.",
            readonly=True,
            style="width: 100%;",
        ),
        Details(
            Summary("Try to recall before reveal"),
            Label(_for="definition")(
                "Definition (Changeable, save using either buttons)"
            ),
            Textarea(
                id="definition",
                name="definition",
                placeholder="Write your own definitions in here.",
                required=True,
                minlength="1",
                style="resize: none;",
            )(card["back"]),
            Div(style="display: flex; gap: 1rem;")(
                Input(
                    data_on_click=(post(f"/read/{num}/forgot", contentType="form"),),
                    type="submit",
                    formaction=f"/read/{num}/forgot",
                    formmethod="post",
                    value="I forgot!",
                ),
                Input(
                    data_on_click=(post(f"/read/{num}/remembered", contentType="form")),
                    type="submit",
                    formaction=f"/read/{num}/remembered",
                    formmethod="post",
                    value="I remembered!",
                ),
            ),
        ),
    )


@read_rt.post("/{num:int}/save")
async def save(auth, num: int, word: str, definition: str):
    if not word and not definition:
        return Redirect(chapter(auth, num=num))

    card = Card()

    db.get(auth).execute(
        """
        INSERT INTO deck (id, front, back, state, step, stability, difficulty, due, last_review)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            card.card_id,
            word,  # front
            definition,  # back
            card.state,
            card.step,
            card.stability,
            card.difficulty,
            # datetime UTC object → str
            card.due.strftime("%Y-%m-%d %H:%M:%S"),  # due
            card.last_review,
        ),
    )

    relay.publish(f"read.{auth}.{num}", word)

    return Redirect(f"/read/{num}?word={word}")


@read_rt.post("/{num:int}/remembered")
async def remembered(auth, num: int, word: str, definition: str):
    rate_card(auth, num, word, definition, forgot=False)
    return Redirect(f"/read/{num}?word={word}")


@read_rt.post("/{num:int}/forgot")
async def forgot(auth, num: int, word: str, definition: str):
    rate_card(auth, num, word, definition, forgot=True)
    return Redirect(f"/read/{num}?word={word}")


def rate_card(auth, num: int, word: str, definition: str, forgot: bool = False):
    if not word and not definition:
        return Redirect(chapter(auth, num=num))

    query = list(
        db.get(auth).query(
            """
                SELECT id, state, step, stability, difficulty, due, last_review
                FROM deck
                WHERE front = ?
            """,
            (
                word,  # front
            ),
        ),
    )[0]

    card = Card(
        query["id"],
        query["state"],
        query["step"],
        query["stability"],
        query["difficulty"],
        # str → datetime UTC object
        datetime.strptime(query["due"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        ),
        datetime.strptime(query["last_review"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
        if query["last_review"]
        else None,
    )

    settings = list(
        db.get(auth).query(
            "SELECT setting, value FROM settings",
        ),
    )

    for s in settings:
        if s["setting"] == "desired_retention":
            desired_retention = s["value"]
        if s["setting"] == "parameters":
            parameters = [float(p) for p in s["value"].split(",")]

    scheduler = Scheduler(desired_retention=desired_retention, parameters=parameters)

    card, review_log = scheduler.review_card(
        card, Rating.Good if not forgot else Rating.Again
    )

    db.get(auth).execute(
        """
            UPDATE deck
            SET back=?, state=?, step=?, stability=?, difficulty=?, due=?, last_review=?
            WHERE front=?
        """,
        (
            definition,  # back
            card.state,
            card.step,
            card.stability,
            card.difficulty,
            card.due.strftime("%Y-%m-%d %H:%M:%S"),  # datetime UTC object to string
            card.last_review.strftime("%Y-%m-%d %H:%M:%S")
            if card.last_review
            else None,
            word,  # front
        ),
    )

    db.get(auth).execute(
        """
            INSERT INTO review_log (card_id, rating, review_datetime, review_duration)
            VALUES (?, ?, ?, ?)
        """,
        (
            review_log.card_id,
            review_log.rating,
            review_log.review_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            review_log.review_duration,
        ),
    )

    relay.publish(f"read.{auth}.{num}", word)
