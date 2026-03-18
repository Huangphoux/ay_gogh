from starhtml import *
from shared import db, html_header, html_footer
from math import ceil

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
                H1("Test", id="main-heading"),
                Figure(
                    Table(
                        Thead(Tr(Th(h.title()) for h in header)),
                        Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
                    ),
                )
                if tests
                else P("You haven't taken any tests yet!"),
                A("Take a Test", _class="button", href=intro),
            ),
            html_footer(sess),
        ),
    )


@test_rt.get("/intro")
def intro(sess):
    # last_form = (
    #     db.get(sess["name"])
    #     .execute("SELECT form FROM test WHERE day = (SELECT MAX(day) FROM test)")
    #     .get
    # )
    db.get(sess["name"]).execute(
        """
            INSERT OR REPLACE INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
            VALUES (CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("a", 0, 0, 0, 0, 0, 0),
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
                    "Each test item has a target word in **bold** font followed by an example sentence which uses this target word. Below the example sentence are four answer choices. ",
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
    last_test = list(
        db.get(sess["name"]).query(
            "SELECT * FROM test WHERE day = (SELECT MAX(day) FROM test)"
        )
    )[0]

    last_num = last_test["progress"]
    next_q = list(db.app.query(f"SELECT * FROM form_a WHERE number = {last_num + 1}"))[
        0
    ]

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
                        P(data_markdown=True)(
                            f"**{next_q['lemma']}**: {next_q['question']}",
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
        db.app.query(f"SELECT answer FROM form_a WHERE number = {last_num + 1}")
    )[0]

    lv_num = ceil((last_num + 1) / 20)
    
    result = 1 if choice == next_q["answer"] else 0

    db.get(sess["name"]).execute(
        f"""
            INSERT OR REPLACE INTO test (day, progress, lv{lv_num})
            VALUES (CURRENT_DATE, ?, ?)
        """,
        (last_num + 1, last_test[f"lv{lv_num}"] + result),
    )
