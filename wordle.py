import random
from load_env import is_debug
from starhtml import *
from starhtml.tags import FT
from shared import db, relay, template


rt: APIRouter = APIRouter("/wordle")


@rt.get("/")
def wordle(auth):
    return template(f"NGSL Wordle", wordle_main(auth), auth)


@rt.get("/cqrs")
@sse
async def cqrs(req, auth):
    async for _, data in relay.subscribe(f"wordle.{auth}"):
        yield elements(
            wordle_main(auth, data["game_state"] if "game_state" in data else None),
            selector="main",
            use_view_transition=True,
        )


def set_new_word(auth):
    word: str = random.choice(
        tuple(
            x["lemma"]
            for x in db.app.query(
                "SELECT lemma FROM ngsl WHERE LENGTH(lemma) BETWEEN 4 AND 6"
            )
        )
    )

    db.get(auth).execute(
        "INSERT OR IGNORE INTO wordle (number, guess, is_submitted) VALUES (?, ?, ?)",
        (0, word.upper(), 1),
    )

    for i in range(1, 6 + 1):
        db.get(auth).execute(
            "INSERT OR IGNORE INTO wordle (number, guess, is_submitted) VALUES (?, ?, ?)",
            (i, "", 0),
        )

    return word


def color_row(guess: str, target: str, is_submitted: int = 1) -> list[FT]:
    row: list[FT] = []

    length = len(target)

    for i in range(length):
        color: str = "gray"  # not in target

        try:
            if guess[i] == target[i]:
                color = "lime"  # in target, correct position
            elif guess[i] in target:
                color = "yellow"  # in target, wrong position
            # else:
            #   color = "gray"

            row.append(
                Td(
                    style=f"background-color: {color}; color: light-dark(var(--text),var(--bg));"
                    if is_submitted
                    else ""
                )(guess[i])
            )
        except IndexError:
            row.append(
                Td(style=f"background-color: {color};" if is_submitted else "")("")
            )

    return row


def wordle_main(auth, game_state: bool | None = None):
    guesses = list(db.get(auth).query("SELECT number, guess, is_submitted FROM wordle"))

    if guesses:
        target: str = guesses[0]["guess"]
    else:
        target: str = set_new_word(auth)
        guesses = list(
            db.get(auth).query("SELECT number, guess, is_submitted FROM wordle")
        )

    h1 = H1(
        id="main-heading",
        style=f"view-transition-name: wordle",
    )(f"NGSL Wordle")

    new_word = (
        Button(data_on_click=delete("/wordle/new"))("New Word")
        if game_state is not None
        else None
    )

    end_game_text: str
    if game_state is True:
        end_game_text = "You won!"
    elif game_state is False:
        end_game_text = f"You lost! The word was {target}"

    end_game = P(_class="notice")(end_game_text) if game_state is not None else None

    table = Table(
        data_on_keydown=(
            js("""
               let charCode  = evt.keyCode;
               
               if ((charCode > 64 && charCode < 91) || (charCode > 96 && charCode < 123)){
                   @put(`/wordle/type/${evt.key}`);
               }
                
               if (evt.key === 'Enter') { @put(`/wordle/enter`) };
               
               if (evt.key === 'Backspace') { @put(`/wordle/backspace`) };
               """),
            dict(window=True, debounce=100),
        )
        if game_state is None
        else None,
    )(
        Tbody(
            Style("""
                    me td {
                        width: 10dvh;
                        height: 10dvh;
                        text-align: center;
                        font-size: 2rem;
                    }
            """),
            *(
                Tr(
                    *color_row(
                        row["guess"], target, is_submitted=int(row["is_submitted"])
                    )
                )
                for row in guesses[1:]
            ),
        )
    )

    debug = Details(Summary("Target word"), target) if is_debug else None

    return Main(data_init=get("/wordle/cqrs"))(
        h1,
        end_game,
        new_word,
        table,
        debug,
    )


@rt.delete("/new")
def new(auth):
    db.get(auth).execute(
        "DELETE FROM wordle",
    )

    relay.publish(f"wordle.{auth}", {})


@rt.put("/type/{key:str}")
def type(auth, key: str):
    last: dict = list(
        db.get(auth).query(
            "SELECT MIN(number) AS number, guess FROM wordle WHERE is_submitted=0"
        )
    )[0]

    length: int = int(len(db.get(auth).item("SELECT guess FROM wordle WHERE number=0")))

    if len(last["guess"]) < length:
        db.get(auth).execute(
            "UPDATE wordle SET guess=CONCAT(guess, ?) WHERE number=?",
            (key.upper(), last["number"]),
        )

    relay.publish(f"wordle.{auth}", {})


@rt.put("/enter")
def enter(auth):
    last: dict = list(
        db.get(auth).query(
            "SELECT MIN(number) AS number, guess FROM wordle WHERE is_submitted=0"
        )
    )[0]

    target: dict = list(
        db.get(auth).query(
            "SELECT guess, LENGTH(guess) AS length FROM wordle WHERE number=0"
        )
    )[0]

    if len(last["guess"]) == target["length"]:
        db.get(auth).execute(
            "UPDATE wordle SET is_submitted=1 WHERE number=?",
            (last["number"],),
        )

    game_state: bool | None = None  # True=win, False=lose, None=in progress

    if last["guess"] == target["guess"]:
        game_state = True
    elif int(last["number"]) == 6:
        game_state = False

    relay.publish(f"wordle.{auth}", {"game_state": game_state})


@rt.put("/backspace")
def backspace(auth):
    last: dict = list(
        db.get(auth).query(
            "SELECT MIN(number) AS number, guess FROM wordle WHERE is_submitted=0"
        )
    )[0]

    if len(last["guess"]) > 0:
        db.get(auth).execute(
            "UPDATE wordle SET guess=? WHERE number=?",
            (last["guess"][:-1], last["number"]),
        )

    relay.publish(f"wordle.{auth}", {})
