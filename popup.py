from apswutils.db import NotFoundError
from starhtml import *
from shared import db, relay
import requests
import json
from fsrs import Scheduler, Card, Rating
from datetime import datetime, timezone
import simplemma

rt: APIRouter = APIRouter("/read")  # so you can have identical APIRouter


@rt.get("/{num:int}/open")
def open(auth, num: int, word: str):
    relay.publish(f"read.{auth}.{num}", word)  # pointerup→open()→cqrs()→popup_view()


@rt.get("/{num:int}/close")
def close(auth, num: int):
    relay.publish(f"read.{auth}.{num}", "")


@rt.patch("/{num:int}/close")
def close_save(auth, num: int, front: str, back: str):
    db.get(auth).execute("UPDATE deck SET back=? WHERE front=?", (back, front))

    relay.publish(f"read.{auth}.{num}", "")


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


def wiktionary_view(word: str, num: int):
    try:
        lv = db.app.item("SELECT level FROM ngsl WHERE lemma = ?", (word,))
    except NotFoundError:
        lv = None

    definition = fetch_definition(word)

    return Form(_class="notice modal")(
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
                    f"if (evt.target.value !== \"\" ) {{ $word = evt.target.value; @get('/read/{num}/open') }};"
                ),
                dict(debounce=500),
            ),
        ),
        Label(_for="back")("Definition"),
        Textarea(
            id="back",
            name="back",
            placeholder="Write your definition in here.",
            required=True,
            style="resize: none;",
            data_ignore_moprh=True,
        ),
        Details(open=True)(
            Summary("Wiktionary"),
            Ul(
                style="max-height: 20vh; overflow: auto",
                data_on_pointerup=(
                    f"if ($word !== \"\" ) {{ @get('/read/{num}/open') }};"
                ),
            )(
                *(Li(d) for d in definition),
            )
            if definition
            else P("Sorry, couldn't find this word in the dictionary."),
        ),
        Div(style="display: flex; gap: 1rem;")(
            Button(_class="outline", data_on_pointerdown=get(f"/read/{num}/close"))(
                "Close"
            ),
            Button(data_on_pointerdown=post(f"/read/{num}/save", contentType="form"))(
                "Save"
            ),
            Div(
                style=" display: grid; place-content: center; ",
            )(f"✅ NGSL Level {lv}" if lv else "❌ Not in NGSL"),
        ),
    )


def not_new_day_view(num: int):
    return Form(_class="notice modal")(
        P(
            "※ ",
            Span(_class="n0t-y3t")("Yellow background"),
            ": the word can't be revealed until tomorrow.",
            Br(),
        ),
        Button(data_on_pointerdown=get(f"/read/{num}/close"))("Close"),
    )


def not_due_view(num: int, due: str):
    time_delta = datetime.strptime(due, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=timezone.utc
    ) - datetime.now(timezone.utc)

    return Form(_class="notice modal")(
        Small(
            "※ ",
            Span(_class="n0t-du3")("Green background"),
            ": the word is not due for a review yet.",
        ),
        P(
            f"Next review is in {str(time_delta).split('.')[0]}."
        ),  # take only what is before the point
        Button(data_on_pointerdown=get(f"/read/{num}/close"))("Close"),
    )


def retired_view(num: int, front: str, back: str):
    return Form(_class="notice modal")(
        Small(
            " ※ ",
            Span(_class="r3t1r3")("Magenta background"),
            ": the word is retired, meaning you won't have to review it anymore.",
        ),
        P(_class="notice")(f"Word: {front}"),
        Input(type="hidden", id="front", name="front", value=front),
        Label(_for="back")("Definition (Changeable, save using either buttons)"),
        Textarea(
            id="back",
            name="back",
            placeholder="Write your own definitions in here.",
            required=True,
            style="resize: none;",
        )(back),
        Div(style="display: flex; gap: 1rem;")(
            Button(
                _class="outline",
                data_on_pointerdown=patch(f"/read/{num}/close", contentType="form"),
            )("Close"),
            Button(
                data_on_pointerdown=delete(f"/read/{num}/retire", contentType="form")
            )("Unretire"),
        ),
    )


def due_view(num: int, front: str, back: str):

    delete_msg = "You are about to delete this word off your memory. \
This action is NOT reversible. Are you sure about this decision?"

    return Form(_class="notice modal")(
        Small(
            "※ ",
            Span(_class="du3")("Red background"),
            ": the word is due for a review.",
        ),
        P(_class="notice")(f"Word: {front}"),
        Input(type="hidden", id="front", name="front", value=front),
        Details(name="due")(
            Summary("Try to recall before reveal"),
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
                    data_on_pointerdown=patch(
                        f"/read/{num}/forgot", contentType="form"
                    ),
                )("I forgot! 👎"),
                Button(
                    _class="outline",
                    data_on_pointerdown=patch(
                        f"/read/{num}/remembered", contentType="form"
                    ),
                )("I remembered! 👍"),
            ),
        ),
        Details(name="due")(
            Summary("More actions"),
            Div(style="display: flex; gap: 1rem; justify-content: space-between;")(
                Button(
                    data_on_pointerdown=patch(f"/read/{num}/retire", contentType="form")
                )("Retire 💤"),
                Button(
                    _class="outline",
                    data_on_pointerdown=js(f"confirm('{delete_msg}')").if_(
                        (delete(f"/read/{num}/delete", contentType="form")), ""
                    ),
                )("⚠️ DELETE ⚠️"),
            ),
        ),
        Button(data_on_pointerdown=get(f"/read/{num}/close"))("Close"),
    )


def popup_view(auth, num: int, word: str = ""):
    if not word:  # default view
        return P(_class="notice")(
            "Select a word to look up its definitions, \
            save it in your memory, then review it in the future."
        )

    if " " in word:
        return Form(_class="notice modal")(
            P(
                "You cannot collect a phrase that has a space in it, only a single word."
            ),
            Button(data_on_pointerdown=get(f"/read/{num}/close"))("Close"),
        )

    try:
        card = list(
            db.get(auth).query(
                """
                SELECT
                    front, back, due, last_review, retire,
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

    # if not card["is_new_day"]: # DEBUG, don't delete, just comment it out
    #     return not_new_day_view(num) # DEBUG, don't delete, just comment it out

    if not card["is_due"]:
        return not_due_view(num, card["due"])

    if card["retire"]:
        return retired_view(num, card["front"], card["back"])

    return due_view(num, card["front"], card["back"])


@rt.delete("/{num:int}/delete")
async def delete_word(auth, num: int, front: str, back: str):
    db.get(auth).execute("DELETE FROM deck WHERE front=?", (front,))

    relay.publish(f"read.{auth}.{num}", front)


@rt.patch("/{num:int}/retire")
async def retire(auth, num: int, front: str, back: str):
    db.get(auth).execute(
        "UPDATE deck SET back=?, retire=? WHERE front=?", (back, 1, front)
    )

    relay.publish(f"read.{auth}.{num}", front)


@rt.delete("/{num:int}/retire")
async def unretire(auth, num: int, front: str, back: str):
    db.get(auth).execute(
        "UPDATE deck SET back=?, retire=? WHERE front=?", (back, 0, front)
    )

    relay.publish(f"read.{auth}.{num}", front)


@rt.post("/{num:int}/save")
async def save(auth, num: int, front: str, back: str):
    card = Card()

    db.get(auth).execute(
        """
        INSERT INTO deck (id, front, back, state, step, stability, difficulty, due, last_review, retire)
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
            0,  # retire
        ),
    )

    relay.publish(f"read.{auth}.{num}", front)


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

    relay.publish(f"read.{auth}.{num}", front)
