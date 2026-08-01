from starhtml import *
from test import is_last_finished
from shared import db
from test import get_last_test
from math import ceil
from apswutils.db import NotFoundError

rt: APIRouter = APIRouter("/")


def hero_page():
    hero = Section(
        style="display: grid; place-items: center; text-align: center; margin-top: 0"
    )(
        H1(id="main-content")("Just Read."),
        Small("It's that simple."),
        P("Read. Collect. Review. Rinse and repeat."),
        A(href="/auth/signup", _class="button")("Sign up"),
        Video(style="padding-top: 1rem")(
            width="1280", height="720", playsinline=True, controls=True
        ),
    )

    introduction = P(style="text-align: center")(
        B("Ay Gogh!"),
        " is a English learning platform,\
                      created to promote the input-driven immersion-based language learning method.",
    )

    nature_method = Section(
        Aside(_class="notice")(
            "Bite-sized reading materials with the ",
            A(href="https://archive.org/details/english-by-the-nature-method/")(
                "English by the Nature Method"
            ),
        ),
        Img(width="400", height="200")(),
    )

    ngsl = Section(
        Aside(_class="notice")(
            "Supercharge your vocabulary acquisition with the ",
            A(href="https://www.newgeneralservicelist.com/new-general-service-list")(
                "NGSL Word List"
            ),
        ),
        Img(width="400", height="200")(),
    )

    fsrs = Section(
        Aside(_class="notice")(
            "Remember your words forever with the ",
            A(
                href="https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler"
            )("FSRS Algorithm"),
        ),
        Img(width="400", height="200")(),
    )

    standard_ebooks = Section(
        Aside(_class="notice")(
            "Explore English literature with the ",
            A(href="https://standardebooks.org/")("Standard Ebooks"),
        ),
        Img(width="400", height="200")(),
    )
    testimonials = Section(
        Blockquote(
            P("Oh yeah, Ay Gogh! is great. What else can I not say about it?"),
            P(Cite("– Random guy of the street")),
        ),
    )
    last_chance = Section(style="display: grid; place-items: center")(
        P(_class="notice")("It's time for you to actually sign up now."),
        P("It's free. Did you know that?"),
        A(href="/auth/signup", _class="button")("Sign up"),
    )

    return Main(
        hero,
        Section(
            introduction,
            nature_method,
            ngsl,
            fsrs,
            # standard_ebooks,
            testimonials,
            last_chance,
        ),
    )


def profile_page(auth):
    last_test = get_last_test(auth)

    sum_done = db.get(auth).item("SELECT COUNT(done) FROM chapter")

    test = Section(
        H2(style=f"view-transition-name: test")(
            A(href="/test/")(
                "Test",
                f" ({(last_test['result'] / 100):.0%})"
                if last_test and last_test["progress"] == 100
                else None,
            )
        ),
        P(_class="notice")(
            "As a new user, you should take a test to measure your core vocabulary knowledge!"
        )
        if is_last_finished(auth) is None
        else P(style="text-align: center;")(
            f"You know {(last_test['result'] / 100):.0%} of NGSL words!"
        ),
    )

    try:
        chap_done_latest = db.get(auth).item(
            "SELECT number FROM chapter WHERE done=(SELECT MAX(done) FROM chapter)"
        )
    except NotFoundError:
        chap_done_latest = None

    read = Section(
        H2(style=f"view-transition-name: read")(
            A(
                href="/read/"
                if not chap_done_latest
                else f"/read/?p={ceil(chap_done_latest / 10) - 1}"
            )(f"Read", f" ({sum_done / 60:.0%})" if sum_done else None)
        ),
        P(style="text-align: center;")(f"Progress: {sum_done} out of 60 chapters!"),
    )

    wordle = Section(
        H2(style=f"view-transition-name: wordle")(A(href="/wordle")("NGSL Wordle")),
        P(style="text-align: center;")(f"Play a game of Wordle using only NGSL words!"),
    )

    try:
        chapter_sql = list(
            db.get(auth).query(
                "SELECT number, progress, lines FROM chapter WHERE progress<>1 AND done IS NULL"
            )
        )
        chapter_count = len(chapter_sql)

    except NotFoundError:
        chapter_sql = None

    incomplete_chapters = (
        Details(
            Summary(
                f"You have {chapter_count} incomplete chapter{'s' if chapter_count > 1 else ''}."
            ),
            Ul(
                *(
                    Li(
                        A(href=f"/read/{chap['number']}")(f"Chapter {chap['number']}"),
                        f" is {chap['progress'] / chap['lines']:.0%} complete",
                    )
                    for chap in chapter_sql
                ),
            ),
        )
        if chapter_sql
        else None
    )

    try:
        word_count = len(
            list(
                db.get(auth).query(
                    """
    SELECT
        is_retired,
        CASE WHEN datetime() > due THEN 1 ELSE 0 END AS is_due,
                -- datetime now is after due
        CASE WHEN (last_review IS NULL AND julianday('now') - julianday(due) < 1) THEN 0 ELSE 1 END AS is_new_day
                --  no last_review       &   it has been 24 hours
    FROM deck
    WHERE is_due=1 AND is_new_day=1 AND is_retired=0
    """
                ),
            )
        )

    except IndexError:
        word_count = None

    due_words = (
        P(_class="notice")(f"You have {word_count} word{'s' if word_count > 1 else ''} due today.")
        if word_count
        else None
    )

    return Main(
        H1(id="main-heading")(f"Profile"),
        incomplete_chapters,
        due_words,
        Section(
            Style("""
                    me {
                        display: grid;
                        /* grid-auto-flow: column;
                        align-items: stretch; */
                        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));

                        gap: 3rem;

                        & section {
                            border: var(--border-width) solid var(--border);
                            padding: 0;
                            margin: 0;
                            text-align: center;
                        }
                    }
            """),
            test,
            read,
            wordle,
        ),
    )
