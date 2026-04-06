from starhtml import *


def set_name(req, sess):
    name = req.scope["name"] = sess.get("name", None)
    if not name:
        return Redirect("/")


auth_bware = Beforeware(
    set_name,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        "/",
        "/auth/login",
        "/auth/login_process",
        "/auth/signup",
        "/auth/signup_process",
    ],
)


from starlette_cramjam.compression import Compression
from starlette_cramjam.middleware import CompressionMiddleware

app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    debug=False,
    # devtools=True,
    datastar="cdn", # patches is needed for DevTools
    # devtools.py, devtools_css = (_DEVTOOLS_DIR / "devtools.css").read_text(encoding="utf-8")
    # mainly my fault for setting the locale to Japanese, setting the encoding to cp932
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    # exception_handlers={
    #     code: lambda req, exc: Redirect("/")
    #     for code in range(400, 500 + 1)  # DEBUG
    # },
    middleware=(
        Middleware(
            CompressionMiddleware,
            compression=[Compression.br, Compression.zstd, Compression.gzip],
            compression_level=10,
        ),
    ),
    static_path="static",
    hdrs=(  # keep / in href, if not, /auth/custom.css
        Link(rel="stylesheet", href="/custom.css"),
        Link(rel="icon", href="https://fav.farm/✅"),  # favicon
        Link(rel="stylesheet", href="https://cdn.simplecss.org/simple.min.css"),
    ),
    sess_https_only=False,  # set Secure flag on cookies
    same_site="strict",
)

# Add routes to app
from auth import auth_rt
from test import test_rt
from read import read_rt

auth_rt.to_app(app)
test_rt.to_app(app)
read_rt.to_app(app)


from test import is_last_finished

from shared import html_header, html_footer, is_signed_in, db


# Page for guests
@rt
def index(req, sess):
    if not is_signed_in(req, sess):
        return (
            Title(f"Home: Ay Gogh"),
            Body(
                A(Strong("Jump to content"), href="#main-content", cls="skip-link"),
                html_header(),
                Main(
                    Section(
                        style="display: grid; place-items: center; text-align: center; margin-top: 0"
                    )(
                        H1(id="main-content")("Just Read."),
                        Small("It's that simple."),
                        P("Read. Collect. Review. Rinse and repeat."),
                        A(href="/auth/signup", _class="button")("Sign up"),
                        Video(style="padding-top: 1rem")(
                            width="1280", height="720", playsinline=True, controls=True
                        )(),
                    ),
                    Section(
                        P(style="text-align: center")(
                            B("Ay Gogh!"),
                            " is a English learning platform, created to promote the input-driven immersion-based language learning method.",
                        ),
                        Section(
                            Aside(_class="notice")(
                                "Bite-sized reading materials with the ",
                                A(
                                    href="https://archive.org/details/english-by-the-nature-method/"
                                )("English by the Nature Method"),
                            ),
                            Img(width="400", height="200")(),
                        ),
                        Section(
                            Aside(_class="notice")(
                                "Supercharge your vocabulary acquisition with the ",
                                A(
                                    href="https://www.newgeneralservicelist.com/new-general-service-list"
                                )("NGSL Word List"),
                            ),
                            Img(width="400", height="200")(),
                        ),
                        Section(
                            Aside(_class="notice")(
                                "Remember your words forever with the ",
                                A(
                                    href="https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler"
                                )("FSRS Algorithm"),
                            ),
                            Img(width="400", height="200")(),
                        ),
                        Section(
                            Aside(_class="notice")(
                                "Explore English literature with the ",
                                A(href="https://standardebooks.org/")(
                                    "Standard Ebooks"
                                ),
                            ),
                            Img(width="400", height="200")(),
                        ),
                        Section(
                            Blockquote(
                                P(
                                    "Oh yeah, Ay Gogh is great. What else can I not say about it?"
                                ),
                                P(Cite("– Random guy of the street")),
                            ),
                        ),
                        Section(style="display: grid; place-items: center")(
                            P(_class="notice")(
                                "It's time for you to actually sign up now."
                            ),
                            P("It's free. Did you know that?"),
                            A(href="/auth/signup", _class="button")("Sign up"),
                        ),
                    ),
                ),
                html_footer(),
            ),
        )

    from apswutils.db import NotFoundError

    try:
        test_done = db.get(sess["name"]).item(
            "SELECT lv1 + lv2 + lv3 + lv4 + lv5 FROM test WHERE day = (SELECT MAX(day) FROM test)"
        )
    except NotFoundError:
        test_done = None

    chap_done = db.get(sess["name"]).item("SELECT SUM(done) FROM chapter")
    if not chap_done:
        chap_done = 0

    return (
        Title("Profile: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1(id="main-heading")(f"{sess['name']}'s profile"),
                Section(
                    H2(
                        A(href="/test/")(
                            "Test", f" ({(test_done / 100):.0%})" if test_done else None
                        )
                    ),
                    P(_class="notice")(
                        "As a new user, you should take a test to measure your core vocabulary knowledge."
                    )
                    if is_last_finished(sess) is None
                    else None,
                ),
                Section(
                    H2(
                        A(href="/read/")(
                            f"Read", f" ({chap_done / 60:.0%})" if chap_done else None
                        )
                    ),
                    P(f"Progress: {chap_done} out of 60 chapters."),
                ),
            ),
            html_footer(sess),
        ),
    )


if __name__ == "__main__":
    serve(port=1984)

    # Clean-up after exiting
    import os, shutil

    os.remove("./.sesskey")
    shutil.rmtree("__pycache__")
