from fastcore.all import timed_cache
from shared import html_header, html_footer
from starhtml import *
from auth import auth_rt
from test import test_rt


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
                "In the meantime, here's a random image of a cat provided by CATAAS, Cat-as-a-Service."
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
app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    devtools=False,
    # devtools.py, devtools_css = (_DEVTOOLS_DIR / "devtools.css").read_text(encoding="utf-8")
    # mainly my fault for setting the locale to Japanese, setting the encoding to cp932
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={404: not_found},
    middleware=(compression(gzip=False, zstd=False, brotli_quality=11),),
    static_path="static",
    hdrs=(  # keep / in href, if not, /auth/custom.css
        Link(rel="icon", href="https://fav.farm/🔥"),  # favicon
        Link(rel="stylesheet", href="/simple.min.css"),
        Link(rel="stylesheet", href="/custom.css"),
    ),
    sess_https_only=False,  # set Secure flag on cookies
    same_site="strict",
    debug=False,
)

auth_rt.to_app(app)
test_rt.to_app(app)


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
