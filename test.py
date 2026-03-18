from starhtml import *
from shared import db, html_header, html_footer
from math import ceil
from random import choice

test_rt: APIRouter = APIRouter("/test")
header = ["day", "form", "progress", "lv1", "lv2", "lv3", "lv4", "lv5"]


@test_rt.get("/")
def test(sess):
    tests = list(db.get(sess["name"]).query("SELECT * FROM test"))

    return (
        Title(f"Test: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                A("< Profile", href="/auth/profile"),
                H1("Test", id="main-heading"),
                Figure(
                    Table(
                        Thead(Tr(Th(h.title()) for h in header)),
                        Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
                    ),
                )
                if tests
                else None,
                P(A("Take a test", _class="button", href=intro)),
                P(
                    "※ You may not take a new test if it hasn't been 2 months since your last test."
                ),
            ),
            html_footer(sess),
        ),
    )


@test_rt.get("/intro")
def intro(sess):
    last_date = list(
        db.get(sess["name"]).query("""
            SELECT progress, julianday('now') - julianday(day) AS diff
            FROM test WHERE day = (SELECT MAX(day) FROM test)
        """)
    )

    if last_date:
        if last_date[0]["progress"] < 100:  # last test is not finished
            return Redirect(progress)
        if last_date[0]["diff"] < 60:  # two months hasn't passed
            return Redirect(test)

    db.get(sess["name"]).execute(
        """
            INSERT OR REPLACE INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
            VALUES (CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?)
        """,
        # ("a", 0, 0, 0, 0, 0, 0),
        (choice("abc"), 91, 0, 10, 20, 0, 0),  ### DEBUG
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
                    "Each test item has a target word in **bold** font followed by an example sentence which uses this target word. Below the example sentence are four answer choices.",
                    data_markdown=True,
                ),
                Ul(
                    Li(
                        "Click the answer choice that best matches the meaning of the target word."
                    ),
                    Li(
                        "You should answer every question. If you do not know the meaning of a word, carefully consider the four choices and make your best guess. "
                    ),
                    Li(
                        "There is no time limit. Most would finish in 20 to 30 minutes.",
                    ),
                ),
                A("Start", _class="button", href=progress),
            ),
            html_footer(sess),
        ),
    )


@test_rt.get("/progress")
def progress(sess):
    last_date = list(
        db.get(sess["name"]).query("""
            SELECT progress, julianday('now') - julianday(day) AS diff
            FROM test WHERE day = (SELECT MAX(day) FROM test)
        """)
    )

    if last_date and last_date[0]["progress"] == 100:
        if last_date[0]["diff"] < 60:
            return Redirect(result)
        else:
            return Redirect(intro)
        
    try:
        last_test = list(
            db.get(sess["name"]).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return Redirect("/auth/profile")

    last_num = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT * FROM form_{last_test['form']} WHERE number = {last_num + 1}"
        )
    )[0]

    return (
        Title(f"Test, Progress {last_num + 1}/100: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1(f"Question {last_num + 1} / 100", id="main-heading"),
                Form(action=progress_process, method="post")(
                    Fieldset(
                        Legend("Select the meaning of the bolded words"),
                        P(
                            Strong(style="font-size:3rem")(next_q["lemma"]),
                            Div(data_markdown=True)(next_q["question"]),
                        ),
                        *[
                            (
                                Input(
                                    type="radio",
                                    name="choice",
                                    value=next_q[answer],
                                    id=answer,
                                    required=True,
                                ),
                                Label(next_q[answer], _for=answer),
                                Br(),
                            )
                            for answer in "abcd"
                        ],
                    ),
                    Button("Advance"),
                ),
            ),
            html_footer(sess),
        ),
    )


@test_rt.post("/progress_process")
def progress_process(choice: str, sess):
    if not choice:
        Redirect(progress)

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

    lv_num = ceil((last_num + 1) / 20)

    lvs = {"lv" + lv: last_test["lv" + lv] for lv in "12345"}

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

    return Redirect(progress)


@test_rt.get("/result")
def result(sess):
    try:
        last_test = list(
            db.get(sess["name"]).query(
                "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
            )
        )[0]
    except IndexError:
        return Redirect("/auth/profile")

    return (
        Title(f"Test, Result: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Result", id="main-heading"),
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
                P(
                    Span(style="color:red; font-weight: bold")("Red-highlighted"),
                    ": score is below 80%. Target your study around these.",
                ),
                A("Return", href="/auth/profile", _class="button"),
            ),
            html_footer(sess),
        ),
    )
