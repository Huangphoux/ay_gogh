from starhtml import *
from shared import db, relay, template
from math import ceil
from random import choice

test_rt: APIRouter = APIRouter("/test")


def get_last_test(auth):
    try:
        last_test = list(
            db.get(auth).query(
                """
                    SELECT *, lv1 + lv2 + lv3 + lv4 + lv5 AS result 
                    FROM test
                    WHERE day = (SELECT MAX(day) FROM test)
                """
            )
        )[0]
    except IndexError:
        last_test = None

    return last_test


@test_rt.get("/")
def test(auth):
    header = ["number", "form", "progress", "lv1", "lv2", "lv3", "lv4", "lv5"]

    tests = list(db.get(auth).query("SELECT * FROM test"))

    last_test = get_last_test(auth)
    result = last_test["result"]
    progress = last_test["progress"]

    main = Main(
        H1("Test", id="main-heading"),
        A(_class="button", href="/test/intro")(
            "Continue last test" if last_test and progress != 100 else "Take a test",
        ),
        Figure(style="max-height: 50vh; overflow: auto")(
            Table(
                Thead(Tr(Th(h.title()) for h in header)),
                Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
            ),
        )
        if tests
        else None,
        Section(
            H2("Your result"),
            P(
                Span(style="color:red; font-weight: bold")("Red-highlighted"),
                ": score < 80%. Target your study around those levels.",
            ),
            Ul(
                *(
                    Li(
                        f"Level {num}: ",
                        f"{last_test[f'lv{num}'] / 20:.0%}",
                        style="color:red; font-weight: bold; font-size: 2rem"
                        if last_test[f"lv{num}"] / 20 < 0.8
                        else None,
                    )
                    for num in "12345"
                ),
            ),
            P(
                style="color:red; font-weight: bold; font-size: 2rem"
                if result and result < 80
                else None,
            )(f"You know {result}% of NGSL words.")
            if result
            else None,
        )
        if last_test and progress == 100
        else P(_class="notice")(
            "An analysis of your test score will be shown here after you finish."
        ),
    )

    return template("Test", main, auth)


def is_last_finished(auth):
    """
    True: Last test exists, is finished.
    False: Last test exists, not finished.
    None: Last test doesn't exist.
    """

    return get_last_test(auth)["progress"] == 100


@test_rt.get("/intro")
def intro(auth):
    last_test = get_last_test(auth)

    progress = last_test["progress"] if last_test else None

    if progress is None or progress == 100:
        db.get(auth).execute(
            """
                INSERT INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)
            """,
            (choice("abc"), 0, 0, 0, 0, 0, 0),
        )

    if progress and progress < 100:
        return Redirect("/test/progress")

    main = Main(
        H1("Intro", id="main-heading"),
        P("This is a test of basic vocabulary knowledge."),
        P(
            "Each question has a ",
            Strong("bolded"),
            " target word, \
            followed by a sentence which uses this target word. \
            Below the sentence are four answer choices.",
        ),
        Ul(
            Li(
                "Choose the answer that best matches the meaning of the ",
                Strong("bolded"),
                " word.",
            ),
            Li("Answer before continuing."),
            Li("There is no time limit."),
            Li("You won't be able to return to previous answers."),
        ),
        A(_class="button", href="/test/progress")("Start"),
    )

    return template("Test, Intro", main, auth)


@test_rt.get("/progress")
def progress_page(auth):
    if is_last_finished(auth):
        return Redirect(test)

    return template("Test, Progress", auth=auth, main=progress_main(auth))


@test_rt.get("/cqrs")
@sse
async def cqrs(req, auth):
    async for _ in relay.subscribe(f"test.{auth}.progress"):
        yield elements(progress_main(auth), selector="main", use_view_transition=True)


def bold_to_strong(next_q):
    question: str = next_q["question"].replace("*", "</strong>")  # </strong></strong>

    # remove the first /
    for i, char in enumerate(split := list(question)):
        if char == "/":
            split[i] = ""
            break

    return "".join(split)


def progress_main(auth):
    if not (last_test := get_last_test(auth)):
        return Redirect(test)

    progress = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT * FROM form_{last_test['form']} WHERE number = {progress + 1}"
        )
    )[0]

    question = bold_to_strong(next_q)

    return Main(data_init=get("/test/cqrs"))(
        H1(f"Question {progress + 1}", id="main-heading"),
        Form(
            data_on_submit=(
                post("/test/progress_process", contentType="form"),
                js("; document.querySelector('form').reset()"),
            ),
        )(
            Fieldset(
                Legend("What's the meaning of the bolded word?"),
                P(style="margin: 0%")(
                    Strong(next_q["lemma"]),
                    ": ",
                    Span(Safe(question)),
                ),
                Ul(style="list-style-type: none; margin: 0%; padding: 0%")(
                    *[
                        Li(style="display: flex;")(
                            Input(
                                type="radio",
                                name="choice",
                                value=next_q[answer],
                                id=answer,
                                required=True,
                            ),
                            Label(_for=answer, style="padding-left: 0.5rem")(
                                next_q[answer]
                            ),
                        )
                        for answer in "abcd"
                    ],
                ),
            ),
            Button("Next"),
        ),
    )


@test_rt.post("/progress_process")
async def progress_process(auth, choice: str):
    if not choice:
        return Redirect(test)

    last_test = get_last_test(auth)
    progress = last_test["progress"]

    next_q = list(
        db.app.query(
            f"SELECT answer FROM form_{last_test['form']} WHERE number = {progress + 1}"
        )
    )[0]

    lvs: dict[str, int] = {f"lv{i}": last_test[f"lv{i}"] for i in "12345"}

    lv_num = ceil((progress + 1) / 20)  # lv1 is 1→20, lv2 is 21→30
    lvs[f"lv{lv_num}"] += 1 if choice == next_q["answer"] else 0

    db.get(auth).execute(
        "UPDATE test SET progress=?, lv1=?, lv2=?, lv3=?, lv4=?, lv5=? WHERE day=?",
        (
            progress + 1,
            *(lvs[f"lv{i}"] for i in "12345"),
            last_test["day"],
        ),
    )

    if is_last_finished(auth) is True:
        return Redirect(test)
    elif is_last_finished(auth) is False:
        relay.publish(f"test.{auth}.progress", "")
