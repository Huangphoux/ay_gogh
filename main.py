from shared import html_header, html_footer
from starhtml import *


def not_found(req, exc):
    import random

    return Body(
        html_header(),
        Main(
            H1(
                random.choice(
                    (
                        "Hmm… I don't think I have that page!",
                        "I'm pretty sure I don't have that page!",
                        f"I don't think I have that in my system.",
                    )
                )
            ),
            Img(
                title="An image of a cat provided by CATAAS, Cat-as-a-Service.",
                style="display:grid;place-self:center",
                alt="An image of a cat provided by CATAAS, Cat-as-a-Service.",
                src="https://cataas.com/cat?type=square",
            ),
            Figcaption(
                "In the meantime, here's a random image of a cat provided by ",
                A(
                    "CATAAS",
                    href="https://cataas.com/",
                    target="_blank",
                    rel="noreferrer",
                ),
                ", Cat-as-a-Service.",
            ),
        ),
        html_footer(),
    )


def set_name(req, sess):
    name = req.scope["name"] = sess.get("name", None)
    if not name:
        return Redirect("/auth/login")


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
    devtools=False,
    # devtools.py, devtools_css = (_DEVTOOLS_DIR / "devtools.css").read_text(encoding="utf-8")
    # mainly my fault for setting the locale to Japanese, setting the encoding to cp932
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={404: not_found},
    middleware=(
        # compression(brotli_quality=8, zstd_level=8, gzip_level=8), # doesn't compress stream
        Middleware(
            CompressionMiddleware,  # ty:ignore[invalid-argument-type]
            compression=[Compression.br, Compression.zstd, Compression.gzip],
            compression_level=10,
        ),
    ),
    static_path="static",
    hdrs=(  # keep / in href, if not, /auth/custom.css
        Link(rel="icon", href="https://fav.farm/🔥"),  # favicon
        Link(rel="stylesheet", href="/simple.min.css"),
        Link(rel="stylesheet", href="/custom.css"),
    ),
    sess_https_only=False,  # set Secure flag on cookies
    same_site="strict",
)

# Add routes to app
from auth import auth_rt
from test import test_rt

auth_rt.to_app(app)
test_rt.to_app(app)

# Register
from starhtml.plugins import markdown

app.register(markdown)


# Page for guests
@rt
def index():
    return (
        Title(f"Home: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-content", cls="skip-link"),
            html_header(),
            Main(id="main-content")(
                P("This page is in construction.", _class="notice"),
                A("Get started", href="/auth/login", _class="button"),
            ),
            html_footer(),
        ),
    )


if __name__ == "__main__":
    serve(port=1984)

    # Clean-up after exiting
    import os, shutil

    os.remove("./.sesskey")
    shutil.rmtree("__pycache__")
