from starhtml import *
from db import DatabaseDict
from relay import Relay

db = DatabaseDict()
relay: Relay[str] = Relay()


def html_header(sess=None):
    nav: starhtml.tags.FT

    if not sess:
        nav = Nav(
            A("Home", href="/"),
            A("Log In", href="/auth/login"),
        )
    else:
        nav = Nav(
            sess and A("Profile", href="/auth/profile"),  # if … then …
            sess
            and A(
                "Log Out",
                data_on_click=js("confirm('Are you sure?')").if_(
                    get("/auth/logout"), ""
                ),
            ),
        )

    return Header(
        # nav,
        H1("Ay Gogh!"),
    )


def html_footer(sess=None):
    return Footer(
        sess
        and (
            A(
                "Log Out",
                data_on_click=js("confirm('Are you sure?')").if_(
                    get("/auth/logout"), ""
                ),
            ),
            Br(),
        ),
        P(
            A(
                "Ay Gogh!",
                href="https://github.com/Huangphoux/ay_gogh",
                target="_blank",
                rel="noreferrer",
            ),
            " is created by the ❤️ of  ",
            A("huangphoux", href="https://github.com/Huangphoux/"),
            ".",
        ),
    )
