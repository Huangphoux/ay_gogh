from starhtml import *
from shared import db, relay, template
from math import ceil
from random import choice

test_rt: APIRouter = APIRouter("/test")


@test_rt.get("/")
def test(auth):
    tests = list(db.get(auth).query("SELECT * FROM test"))
    header = ["number", "day", "form", "progress", "lv1", "lv2", "lv3", "lv4", "lv5"]

    try:
        last_test = list(
            db.get(auth).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        last_test = None

    main = Main(
        H1("Test", id="main-heading"),
        A(_class="button", href=intro)(
            "Continue last test"
            if last_test and last_test["progress"] != 100
            else "Take a test",
        ),
        Figure(
            Table(
                Thead(Tr(Th(h.title()) for h in header)),
                Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
            ),
        )
        if tests
        else None,
        Section(
            H2("Your latest test's result"),
            P(
                Span(style="color:red; font-weight: bold")("Red-highlighted"),
                ": score < 80%. Target your study around those levels.",
            ),
            Ul(
                *(
                    Li(
                        f"Level {num}: ",
                        f"{last_test[f'lv{num}'] / 20:.0%}"
                        if last_test and last_test["progress"] == 100
                        else None,
                        style="color:red; font-weight: bold; font-size: 2rem"
                        if last_test
                        and last_test["progress"] == 100
                        and last_test[f"lv{num}"] / 20 < 0.8
                        else None,
                    )
                    for num in "12345"
                ),
            ),
        ),
    )

    return template("Test", main, auth)


def is_last_finished(auth):
    """
    True: Last test exists, is finished.
    False: Last test exists, not finished.
    None: Last test doesn't exist.
    """

    try:
        last_test = list(
            db.get(auth).query(
                "SELECT progress FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return None

    return last_test["progress"] == 100


@test_rt.get("/intro")
def intro(auth):
    try:
        last_test = list(
            db.get(auth).query(
                "SELECT progress FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        last_test = None

    last_num = last_test["progress"] if last_test else None

    if last_num is None or last_num == 100:
        db.get(auth).execute(
            """
                INSERT INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)
            """,
            (choice("abc"), 0, 0, 0, 0, 0, 0),  # DEBUG
        )

    if last_num and last_num < 100:
        return Redirect(progress)

    main = Main(
        H1("Intro", id="main-heading"),
        P("This is a test of basic vocabulary knowledge."),
        P(
            "Each test item has a target word in ",
            Strong("bold"),
            " font, followed by a sentence which uses this target word. \
            Below the sentence are four answer choices.",
        ),
        Ul(
            Li(
                "Choose the answer choice that best matches the meaning of the target word."
            ),
            Li("Answer the question before continuing."),
            Li(
                "There is no time limit.",
            ),
        ),
        A(_class="button", href=progress)("Start"),
    )

    return template("Test, Intro", main, auth)


@test_rt.get("/progress")
def progress(auth):
    if is_last_finished(auth):
        return Redirect(test)

    return template("Settings, FSRS", auth=auth, main=progress_main(auth))


@test_rt.get("/cqrs")
@sse
async def cqrs(req, auth):
    async for _ in relay.subscribe(f"test.{auth}.progress"):
        yield elements(progress_main(auth), selector="main", use_view_transition=True)


def progress_main(auth):
    try:
        last_test = list(
            db.get(auth).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return Redirect(test)

    last_num = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT * FROM form_{last_test['form']} WHERE number = {last_num + 1}"
        )
    )[0]

    question: str = next_q["question"].replace("*", "</strong>")  # </strong></strong>
    # remove the first /
    for i, char in enumerate(split := list(question)):
        if char == "/":
            split[i] = ""
            break
    question = "".join(split)

    return Main(data_init=get(cqrs))(
        H1(f"Question {last_num + 1}", id="main-heading"),
        Form(
            data_on_submit=(
                post(progress_process, contentType="form"),
                js("; document.querySelector('form').reset()"),
            ),
        )(
            Fieldset(
                Legend("Choose your answer"),
                P(style="margin: 0%")(
                    Strong(next_q["lemma"]),
                    ": ",
                    Span(Safe(question)),
                ),
                Ul(style="list-style-type: none; margin: 0%; padding: 0%")(
                    *[
                        Li(style="display: flex; align-items: center; gap: 0.5rem")(
                            Input(
                                type="radio",
                                name="choice",
                                value=next_q[answer],
                                id=answer,
                                required=True,
                            ),
                            Label(_for=answer)(next_q[answer]),
                        )
                        for answer in "abcd"
                    ],
                ),
            ),
            Button("Advance"),
        ),
    )


@test_rt.post("/progress_process")
async def progress_process(auth, choice: str):
    if not choice:
        return Redirect(test)

    last_test = list(
        db.get(auth).query("SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)")
    )[0]

    last_num = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT answer FROM form_{last_test['form']} WHERE number = {last_num + 1}"
        )
    )[0]

    lvs = {"lv" + lv: last_test["lv" + lv] for lv in "12345"}

    lv_num = ceil((last_num + 1) / 20)  # lv1 is 1→20, lv2 is 21→30
    lvs[f"lv{lv_num}"] += 1 if choice == next_q["answer"] else 0

    db.get(auth).execute(
        "UPDATE test SET progress=?, lv1=?, lv2=?, lv3=?, lv4=?, lv5=? WHERE day=?",
        (
            last_num + 1,
            lvs["lv1"],
            lvs["lv2"],
            lvs["lv3"],
            lvs["lv4"],
            lvs["lv5"],
            last_test["day"],
        ),
    )

    if is_last_finished(auth) is True:
        return Redirect(test)
    elif is_last_finished(auth) is False:
        relay.publish(f"test.{auth}.progress", "")
