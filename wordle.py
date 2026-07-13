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
        yield elements(wordle_main(auth), selector="main", use_view_transition=True)


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


def wordle_main(auth):
    guesses = list(db.get(auth).query("SELECT number, guess, is_submitted FROM wordle"))

    if guesses:
        target: str = guesses[0]["guess"]
    else:
        target: str = set_new_word(auth)
        guesses = list(
            db.get(auth).query("SELECT number, guess, is_submitted FROM wordle")
        )

    h1 = H1(id="main-heading", style=f"view-transition-name: wordle")(f"NGSL Wordle")

    game_state = get_game_state(auth)
    print(game_state)

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


def get_game_state(auth) -> bool | None:
    """True=win, False=lose, None=in progress"""

    last: dict[str, str] = get_last(auth, is_submitted=True)
    target: str = db.get(auth).item("SELECT guess FROM wordle WHERE number=0")

    if last["guess"] == target:
        return True
    elif last["number"] is not None and int(last["number"]) == 6:
        return False
    else:
        return None


def get_last(auth, is_submitted: bool = False) -> dict[str, str]:
    return list(
        db.get(auth).query(
            f"""
                SELECT {"MAX" if is_submitted else "MIN"}(number) AS number, guess
                FROM wordle
                WHERE {"is_submitted=0" if not is_submitted else "is_submitted=1 AND number<>0"}
            """
        )
    )[0]


def get_target(auth) -> dict[str, str]:
    return list(
        db.get(auth).query(
            "SELECT guess, LENGTH(guess) AS length FROM wordle WHERE number=0"
        )
    )[0]


def get_length(auth) -> int:
    return int(len(db.get(auth).item("SELECT guess FROM wordle WHERE number=0")))


@rt.delete("/new")
def new(auth):
    db.get(auth).execute("DELETE FROM wordle")
    relay.publish(f"wordle.{auth}", {})


@rt.put("/type/{key:str}")
def type(auth, key: str):
    last: dict[str, str] = get_last(auth)

    if len(last["guess"]) < get_length(auth):
        db.get(auth).execute(
            "UPDATE wordle SET guess=CONCAT(guess, ?) WHERE number=?",
            (key.upper(), last["number"]),
        )

    relay.publish(f"wordle.{auth}", {})


@rt.put("/enter")
def enter(auth):
    last: dict[str, str] = get_last(auth)

    if len(last["guess"]) == get_length(auth):
        db.get(auth).execute(
            "UPDATE wordle SET is_submitted=1 WHERE number=?",
            (last["number"],),
        )

    relay.publish(f"wordle.{auth}", {})


@rt.put("/backspace")
def backspace(auth):
    last: dict[str, str] = get_last(auth)

    if len(last["guess"]) > 0:
        db.get(auth).execute(
            "UPDATE wordle SET guess=? WHERE number=?",
            (last["guess"][:-1], last["number"]),
        )

    relay.publish(f"wordle.{auth}", {})
