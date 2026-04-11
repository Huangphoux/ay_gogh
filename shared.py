from starhtml import *
from db import DatabaseDict
from relay import Relay


db = DatabaseDict()
relay: Relay[str] = Relay()


def is_signed_in(req, sess):
    name = req.scope["name"] = sess.get("name", None)

    return True if name else False


def html_header(sess=None):
    nav: starhtml.tags.FT

    if not sess:
        nav = Nav(
            A("Home", href="/"),
            A("Log In", href="/auth/login"),
        )
    else:
        nav = Nav(
            sess and A("Profile", href="/"),  # if … then …
        )

    return Header(
        nav,
        H1("Ay Gogh!"),
        Noscript(P("JavaScript is needed to ensure the best experience.")),
    )


def html_footer(sess=None):
    return Footer(
        sess
        and A(
            "Log Out",
            data_on_click=js("confirm('Are you sure?')").if_(delete("/auth/login"), ""),
        ),
        P(
            A(href="https://github.com/Huangphoux/ay_gogh")("Ay Gogh!"),
            " is created by the ❤️ of  ",
            A(href="https://github.com/Huangphoux/")("huangphoux"),
            ".",
        ),
        P("Copyright © Ay Gogh! 2026"),
    )
