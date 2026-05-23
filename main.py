from load_env import is_debug
from starhtml import *
import os, shutil
from starlette_cramjam.compression import Compression
from starlette_cramjam.middleware import CompressionMiddleware
from test import is_last_finished
from shared import template, is_signed_in, db
from test import get_last_test
from relay_instance import relay

import settings
import read
import test
import auth
import popup


def set_name(req, sess):
    auth = req.scope["auth"] = sess.get("auth", None)
    if not auth:
        return Redirect("/")


auth_bware = Beforeware(
    set_name,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        "/",
        *(
            f"/auth/{path}"
            for path in ("login", "login_process", "signup", "signup_process")
        ),
    ],
)


app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    debug=False,
    # devtools.py, devtools_css = (_DEVTOOLS_DIR / "devtools.css").read_text(encoding="utf-8")
    # mainly my fault for setting the locale to Japanese, setting the encoding to cp932
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={num: lambda req, exc: Redirect("/") for num in range(400, 600)}
    if not is_debug
    else {},
    middleware=(
        Middleware(
            CompressionMiddleware,
            compression=[Compression.br, Compression.zstd, Compression.gzip],
        ),
    ),
    static_path="static",
    # default_hdrs=False,
    hdrs=(  # keep / in href, if not, /auth/custom.css
        Link(rel="stylesheet", href="/custom.css"),
        Link(rel="icon", href="https://fav.farm/📖"),  # favicon
        Link(rel="stylesheet", href="https://cdn.simplecss.org/simple.min.css"),
    ),
    sess_https_only=not is_debug,  # set Secure flag on cookies
    same_site="strict",
    # .sesskey can be read/write by anyone
    # chmod 600 .sesskey to only be able to read/write by owner
    datastar="cdn",
    inline_icons=True,
)

relay.install(app)

auth.rt.to_app(app)
test.rt.to_app(app)
read.rt.to_app(app)
popup.rt.to_app(app)
settings.rt.to_app(app)


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
            P("Oh yeah, Ay Gogh is great. What else can I not say about it?"),
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
            standard_ebooks,
            testimonials,
            last_chance,
        ),
    )


def profile_page(auth):
    last_test = get_last_test(auth)

    sum_done = db.get(auth).item("SELECT SUM(done) FROM chapter")

    test = Section(
        H2(
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
        else None,
    )

    read = Section(
        H2(A(href="/read/")(f"Read", f" ({sum_done / 60:.0%})" if sum_done else None)),
        P(f"Progress: {sum_done} out of 60 chapters."),
    )

    return Main(
        H1(id="main-heading")(f"{auth}'s profile"),
        test,
        read,
    )


@rt
def index(req, sess):
    auth = sess.get("auth", None)

    main = hero_page() if not is_signed_in(req, sess) else profile_page(auth)

    return template("Home", main, auth)


if __name__ == "__main__":
    print(
        "You are currently in DEBUG mode.\n\
The `db` folder will be DELETED after stopping the server.\n\
You have been warned."
    ) if is_debug else None
    
    serve(port=1984)
    # remember to add `server_header=False` to uvicorn.run
    # log_level="error" too

    # Clean-up after exiting

    os.remove("./.sesskey")
    shutil.rmtree("__pycache__")

    db.close_all()
    shutil.rmtree("db") if is_debug else None
