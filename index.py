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
            "As a new user, you should take a test to measure your core vocabulary knowledge."
        )
        if is_last_finished(auth) is None
        else P(style="text-align: center;")(
            f"You know {(last_test['result'] / 100):.0%} of NGSL words."
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
        P(style="text-align: center;")(f"Progress: {sum_done} out of 60 chapters."),
    )

    return Main(
        H1(id="main-heading")(f"{auth}'s profile"),
        Section(_class="profile")(
            test,
            read,
        ),
    )
