from shared import html_header, html_footer
from starhtml import *


def not_found(req, exc):
    return H1("There's no such page like that!")


def set_auth(req, sess):
    auth = req.scope["name"] = sess.get("name", None)
    if not auth:
        return Redirect("/auth/login")


auth_bware = Beforeware(
    set_auth,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        "/",
        "/auth/login",
        "/auth/login_process",
    ],
)

app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={404: not_found},
    middleware=(compression(),),
    static_path="static",
    hdrs=(  # / in href ARE VERY IMPORTANT, DO NOT DELETE THEM
        Link(rel="stylesheet", href="/simple.min.css"),
        Link(rel="stylesheet", href="/custom.css"),
    ),
    sess_https_only=False,  # secure
    same_site="strict",
)
from auth import auth_rt

auth_rt.to_app(app)


@rt
def index():

    return (
        html_header(),
        Main(
            P("This page is in construction.", _class="notice"),
            A("Get started", href="/auth/login", _class="button"),
        ),
        html_footer(),
    )


@rt
def profile(sess):
    return Body(
        html_header,
        Main(
            H1(f"Hello, {sess['name']}"),
            A("Log Out", href="/auth/logout"),
        ),
        html_footer,
    )


if __name__ == "__main__":
    serve(port=1984)
