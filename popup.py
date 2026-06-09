from apswutils.db import NotFoundError
from starhtml import *
from shared import db, relay
import requests
import json
from fsrs import Scheduler, Card, Rating
from datetime import datetime, timezone
import simplemma
from humanize import precisedelta

rt: APIRouter = APIRouter("/read")  # so you can have identical APIRouter


def publish(auth, num: int, word: str = "", bypass: int = 0):
    # pointerup→open()→cqrs()→popup_view()
    relay.publish(f"read.{auth}.{num}", dict(word=word, bypass=bypass))


@rt.get("/{num:int}/open")
def open(auth, num: int, word: str = "", bypass: int = 0):
    publish(auth, num, word, bypass)


@rt.get("/{num:int}/close")
def close(auth, num: int):
    publish(auth, num)


@rt.patch("/{num:int}/close")
def close_save(auth, num: int, front: str, back: str):
    db.get(auth).execute("UPDATE deck SET back=? WHERE front=?", (back, front))
    publish(auth, num)


def fetch_definition(word: str = ""):
    if not word:
        return None

    word = simplemma.lemmatize(word, lang="en") if word else ""

    try:
        fetch = json.loads(
            requests.get(f"https://freedictionaryapi.com/api/v1/entries/en/{word}").text
        )["entries"][0]

        definition = [
            s["definition"]
            for s in fetch["senses"]
            if "(obsolete)" not in s["definition"]
        ]
    except IndexError:
        definition = None

    return definition


def popup_form(num: int, content):
    form = Details(
        open=True,
        popover="manual",
        id="popup",
        data_on_keydown=(
            js(
                f"if ( evt.key === 'Escape' && document.querySelector('#popup').checkVisibility() === true )  \
                {{ @get('/read/{num}/close'); document.querySelector('#popup').hidePopover(); }}"
            ),
            dict(window=True),
        ),
    )(
        Summary(data_text="$searching ? 'Popup (Searching …)' : 'Popup'"),
        Form(content),
    )

    return form


def close_btn(num: int, is_outlined: bool = False, is_save: bool = False):
    if is_save:
        btn = Button(
            data_on_click=(
                js(
                    f"@patch('/read/{num}/close', {{contentType: 'form'}});\
                    document.querySelector('#popup').hidePopover();"
                ),
            ),
        )
    else:
        btn = Button(
            data_on_click=(
                js(
                    f"@get('/read/{num}/close');\
                    document.querySelector('#popup').hidePopover();"
                ),
                dict(prevent=True),
            ),
        )

    return btn(_class="outline" if is_outlined else None)(
        "Close", " & Save" if is_save else ""
    )


def bypass_btn(num: int, word: str = "", is_outlined: bool = False):
    # Review anyway → /open → morph() → chapter_main() → popup_view()
    return Button(
        _class="outline" if is_outlined else None,
        data_on_click=(
            get(f"/read/{num}/open?bypass=1&word={word}"),
            dict(prevent=True),
        ),
    )("Review anyway")


def wiktionary_view(word: str, num: int):
    try:
        lv = db.app.item("SELECT level FROM ngsl WHERE lemma = ?", (word,))
    except NotFoundError:
        lv = None

    definition = fetch_definition(word)

    front_part = (
        Label(_for="front")("Word"),
        Input(
            type="text",
            id="front",
            name="front",
            value=word,
            required=True,
            placeholder="Write the word you want to collect in here.",
            style="width: 100%;",
            data_on_input=(
                js(
                    f"if (evt.target.value !== \"\" )\
                    {{ $word = evt.target.value; @get('/read/{num}/open') }};"
                ),
                dict(debounce=100),
            ),
        ),
    )

    front_part = (
        H2(f"Word: {word}"),
        Input(type="hidden", id="front", name="front", value=word),
    )

    back_part = (
        Label(_for="back")("Definition"),
        Textarea(
            id="back",
            name="back",
            placeholder="Write your definition in here.",
            required=True,
            style="resize: none;",
            data_ignore_moprh=True,
        ),
    )

    wiktionary_part = Details(
        open=True, style="height: 20dvh; resize: vertical; overflow: auto;"
    )(
        Summary(f"Dictionary"),
        Ul(
            data_on_pointerup=(f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};"),
            data_indicator="searching",
        )(
            *(Li(d) for d in definition),
        )
        if definition
        else P("Sorry, couldn't find the word in the dictionary."),
    )

    buttons = Div(style="display: flex; gap: 1rem;")(
        close_btn(num, is_outlined=True),
        Button(data_on_click=post(f"/read/{num}/save", contentType="form"))("Save"),
        Span(style="display: grid; place-items: center;")(
            f"✅ NGSL {f' Level {lv}' if lv > 0 else ''}"
            if lv is not None
            else f"❌ Not in NGSL"
        ),
    )

    content = (front_part, back_part, wiktionary_part, buttons)
    return popup_form(num, content)


def not_new_day_view(num: int, word: str):
    content = (
        # P(
        #     "※ Yellow background: the word can't be reviewed until tomorrow.",
        # ),
        P("This word cannot be reviewed until tomorrow."),
        Div(style="display: flex; gap: 1rem; justify-content: space-between;")(
            close_btn(num),
            bypass_btn(num, word, is_outlined=True),
        ),
    )

    return popup_form(num, content)


def not_due_view(num: int, word: str, due: str):
    time_delta = datetime.strptime(due, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=timezone.utc
    ) - datetime.now(timezone.utc)

    content = (
        # Small(
        #     "※ Green background: the word is not due for a review yet.",
        # ),
        P(f"Next review is in {precisedelta(time_delta)}."),
        Div(style="display: flex; gap: 1rem; justify-content: space-between;")(
            close_btn(num),
            bypass_btn(num, word, is_outlined=True),
        ),
    )

    return popup_form(num, content)


def retired_view(num: int, front: str, back: str):
    small = Small(
        " ※ Blue background: you don't have to review it anymore.",
    )

    front_part = (
        H2(f"Word: {front}"),
        Input(type="hidden", id="front", name="front", value=front),
    )

    back_part = (
        Label(_for="back")("Definition (Changeable, save using either buttons)"),
        Textarea(
            id="back",
            name="back",
            placeholder="Write your own definitions in here.",
            required=True,
            style="resize: none;",
        )(back),
    )

    buttons = Div(style="display: flex; gap: 1rem;")(
        close_btn(num, is_outlined=True, is_save=True),
        Button(data_on_click=delete(f"/read/{num}/retire", contentType="form"))(
            "Unretire"
        ),
    )

    content = (front_part, back_part, buttons)
    return popup_form(num, content)


def due_view(num: int, front: str, back: str, bypass: int):
    delete_msg = "You are about to delete this word off your memory. \
This action is NOT reversible. Are you sure about this decision?"

    small = (
        Small(
            "※ Red background: the word is due for a review.",
        )
        if not bypass
        else None
    )

    front_part = (
        H2(f"Word: {front}"),
        Input(type="hidden", id="front", name="front", value=front),
    )

    rate_part = Details(name="due")(
        Summary("Recall before reveal"),
        Label(_for="back")("Definition (Changeable, save using either buttons)"),
        Textarea(
            id="back",
            name="back",
            placeholder="Write your own definitions in here.",
            required=True,
            minlength="1",
            style="resize: none;",
        )(back),
        Div(style="display: flex; gap: 1rem; justify-content: space-between;")(
            Button(
                data_on_click=patch(f"/read/{num}/forgot", contentType="form"),
            )("I forgot!"),
            Button(
                _class="outline",
                data_on_click=patch(f"/read/{num}/remembered", contentType="form"),
            )("I remembered!"),
        ),
    )

    more_part = Details(name="due")(
        Summary("More actions"),
        Div(style="display: flex; gap: 1rem; justify-content: space-between;")(
            Button(
                title="Retire this word so you don't have to review it anymore.",
                data_on_click=patch(
                    f"/read/{num}/retire",
                    contentType="form",
                ),
            )("Retire"),
            Button(
                _class="outline",
                data_on_pointerdown=js(f"confirm('{delete_msg}')").if_(
                    (delete(f"/read/{num}/delete", contentType="form")), ""
                ),
            )("Delete"),
        ),
    )

    content = (front_part, rate_part, more_part, close_btn(num))
    return popup_form(num, content)


def search_view(num: int):
    buttons = Div(style="display: flex; gap: 1rem;", data_show="!$searching")(
        close_btn(num, is_outlined=True),
        Button(
            data_on_click=get(f"/read/{num}/open", contentType="form"),
            data_indicator="searching",
        )("Search"),
    )

    content = (
        P(data_show="$searching")("Searching the word in your memory …"),
        Label(_for="word", data_show="!$searching")(
            "Write the word you want to search in your memory here."
        ),
        Input(
            type="text",
            id="word",
            name="word",
            minlength="1",
            required=True,
            placeholder="e.g. hawk tuah",
            style="width: 100%;",
            data_show="!$searching",
        ),
        buttons,
    )

    return popup_form(num, content)


def popup_view(auth, num: int, word: str = "", bypass: int = 0):
    if not word:  # default view
        return search_view(num)

    if not word.isalpha():
        content = (
            P(
                "You have not selected a single word. Select a single word to look up its definitions."
            ),
            close_btn(num),
        )
        return popup_form(num, content)

    try:
        card = list(  # this one find the word's card
            db.get(auth).query(
                """
                SELECT
                    front, back, due, last_review, is_retired,
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

    if not card:  # not in memory, hasn't mined yet
        return wiktionary_view(word, num)

    if card["is_retired"]:
        return retired_view(num, card["front"], card["back"])

    if not bypass and not card["is_new_day"]:
        return not_new_day_view(num, word)

    if not bypass and not card["is_due"]:
        return not_due_view(num, word, card["due"])

    return due_view(num, card["front"], card["back"], bypass)


@rt.delete("/{num:int}/delete")
async def delete_word(auth, num: int, front: str):
    db.get(auth).execute("DELETE FROM deck WHERE front=?", (front,))
    publish(auth, num, front)


@rt.patch("/{num:int}/retire")
async def retire(auth, num: int, front: str, back: str):
    db.get(auth).execute(
        "UPDATE deck SET back=?, is_retired=? WHERE front=?", (back, 1, front)
    )
    publish(auth, num, front)


@rt.delete("/{num:int}/retire")
async def unretire(auth, num: int, front: str, back: str):
    db.get(auth).execute(
        "UPDATE deck SET back=?, is_retired=? WHERE front=?", (back, 0, front)
    )
    publish(auth, num, front)


@rt.post("/{num:int}/save")
async def save(auth, num: int, front: str, back: str):
    card = Card()

    db.get(auth).execute(
        """
        INSERT INTO deck (id, front, back, state, step, stability, difficulty, due, last_review, is_retired)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            card.card_id,
            front,
            back,
            card.state,
            card.step,
            card.stability,
            card.difficulty,
            # datetime UTC object → str
            card.due.strftime("%Y-%m-%d %H:%M:%S"),  # due
            card.last_review,
            0,  # is_retired
        ),
    )

    publish(auth, num, front)


@rt.patch("/{num:int}/remembered")
async def remembered(auth, num: int, front: str, back: str):
    rate_card(auth, num, front, back, forgot=False)


@rt.patch("/{num:int}/forgot")
async def forgot(auth, num: int, front: str, back: str):
    rate_card(auth, num, front, back, forgot=True)


def rate_card(auth, num: int, front: str, back: str, forgot: bool = False):
    query = list(
        db.get(auth).query(
            """
                SELECT id, state, step, stability, difficulty, due, last_review
                FROM deck
                WHERE front = ?
            """,
            (front,),
        ),
    )[0]

    card = Card(
        int(query["id"]),
        query["state"],
        query["step"],
        query["stability"] and float(query["stability"]),
        query["difficulty"] and float(query["difficulty"]),
        # str → datetime UTC object
        datetime.strptime(query["due"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        ),
        query["last_review"]
        and datetime.strptime(query["last_review"], "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        ),
    )

    settings = list(db.get(auth).query("SELECT setting, value FROM settings"))

    for s in settings:
        if s["setting"] == "desired_retention":
            desired_retention = float(s["value"])
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
            back,  # back
            card.state,
            card.step,
            card.stability,
            card.difficulty,
            card.due.strftime("%Y-%m-%d %H:%M:%S"),  # datetime UTC object to string
            card.last_review.strftime("%Y-%m-%d %H:%M:%S")
            if card.last_review
            else None,
            front,  # front
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

    publish(auth, num, front)
