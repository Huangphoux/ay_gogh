from starhtml import *
from shared import db, html_header, html_footer, relay
from math import ceil
from random import choice

test_rt: APIRouter = APIRouter("/test")


header = ["day", "form", "progress", "lv1", "lv2", "lv3", "lv4", "lv5"]


@test_rt.get("/")
def test(sess):
    tests = list(db.get(sess["name"]).query("SELECT * FROM test"))

    try:
        last_test = list(
            db.get(sess["name"]).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        last_test = None

    last_finished = last_test and last_test["progress"] == 100

    return (
        Title(f"Test: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Test", id="main-heading"),
                Details(open=last_finished)(
                    Summary("Result of your latest test"),
                    P(
                        Span(style="color:red; font-weight: bold")("Red-highlighted"),
                        ": score is below 80%. Target your study around those levels.",
                    ),
                    Ul(
                        *(
                            Li(
                                f"Level {num}: {last_test[f'lv{num}'] / 20:.0%}",
                                style="color:red; font-weight: bold; font-size: 2rem"
                                if last_test[f"lv{num}"] / 20 < 0.8
                                else None,
                            )
                            for num in "12345"
                        ),
                    ),
                )
                if last_test and last_test["progress"] == 100
                else None,
                Figure(
                    Table(
                        Thead(Tr(Th(h.title()) for h in header)),
                        Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
                    ),
                )
                if tests
                else None,
                P(A(_class="button", href=intro)("Take a test")),
                Ul(
                    Li("You may continue your latest test if hasn't finished yet."),
                    Li("You may not take more than one test in the same day."),
                ),
            ),
            html_footer(sess),
        ),
    )


def is_last_finished(sess):
    """
    True: Last test exists, is finished.
    False: Last test exists, not finished.
    None: Last test doesn't exist.
    """

    try:
        last_test = list(
            db.get(sess["name"]).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return None

    return last_test["progress"] == 100


@test_rt.get("/intro")
def intro(sess):
    last_finished = is_last_finished(sess)

    if last_finished is False:
        return Redirect(progress)
    elif last_finished is True:
        return Redirect(test)

    db.get(sess["name"]).execute(
        """
            INSERT OR REPLACE INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
            VALUES (CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?)
        """,
        (choice("abc"), 97, 0, 0, 0, 0, 0),
    )

    return (
        Title(f"Test, Intro: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Intro", id="main-heading"),
                P("This is a test of basic vocabulary knowledge."),
                P(
                    "Each test item has a target word in ",
                    Strong("bold"),
                    " font, followed by an example sentence which uses this target word. Below the example sentence are four answer choices.",
                ),
                Ul(
                    Li(
                        "Choose the answer choice that best matches the meaning of the target word."
                    ),
                    Li("You should answer every question before continuing."),
                    Li(
                        "There is no time limit, but this should take you 20 to 30 minutes to finish.",
                    ),
                ),
                A(_class="button", href=progress)("Start"),
            ),
            html_footer(sess),
        ),
    )


@test_rt.get("/progress")
def progress(sess):
    if is_last_finished(sess) is True:
        return Redirect(test)

    return progress_view(sess)


@test_rt.get("/cqrs")
@sse
async def cqrs(req, sess):
    async for _ in relay.subscribe(f"test.{sess['name']}.progress"):
        yield elements(progress_view(sess), use_view_transition=True)


def progress_view(sess):
    try:
        last_test = list(
            db.get(sess["name"]).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return Redirect("/")

    last_num = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT * FROM form_{last_test['form']} WHERE number = {last_num + 1}"
        )
    )[0]

    return (
        Title(f"Test, Progress: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(data_init=get(cqrs))(
                H1(f"Question {last_num + 1}", id="main-heading"),
                Form(
                    data_on_submit=(
                        post(progress_process, {"contentType": "form"}),
                        # ; is for seperation
                        js("; document.querySelector('form').reset()"),
                    )
                )(
                    Fieldset(
                        Legend("Choose your answer"),
                        P(style="margin: 0%")(
                            Strong(next_q["lemma"]),
                            ": ",
                            Span(data_markdown=True, style="display: inline-block")(
                                next_q["question"]
                            ),
                        ),
                        Ul(style="list-style-type: none; margin: 0%; padding: 0%")(
                            *[
                                Li(
                                    Input(
                                        type="radio",
                                        name="choice",
                                        value=next_q[answer],
                                        id=answer,
                                        required=True,
                                    ),
                                    Label(
                                        next_q[answer],
                                        _for=answer,
                                    ),
                                )
                                for answer in "abcd"
                            ],
                        ),
                    ),
                    Button("Advance"),
                ),
            ),
            html_footer(sess),
        ),
    )


@test_rt.post("/progress_process")
async def progress_process(sess, choice: str):
    if not choice:
        return Redirect(test)

    last_test = list(
        db.get(sess["name"]).query(
            "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
        )
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

    db.get(sess["name"]).execute(
        """
            INSERT OR REPLACE INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            last_test["day"],
            last_test["form"],
            last_num + 1,
            lvs["lv1"],
            lvs["lv2"],
            lvs["lv3"],
            lvs["lv4"],
            lvs["lv5"],
        ),
    )

    if is_last_finished(sess) is True:
        return Redirect(test)
    elif is_last_finished(sess) is False:
        relay.publish(f"test.{sess['name']}.progress", "")
