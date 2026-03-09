from starhtml import *
from db import DatabaseDict
from relay import Relay

db = DatabaseDict()
relay: Relay[str] = Relay()


def html_header(sess=None):
    return Header(
        Nav(
            sess and A("Profile", href="/profile"),  # if … then …
            sess
            and A(
                "Log Out",
                data_on_click=js("confirm('Are you sure?')").if_(
                    get("/auth/logout"), ""
                ),
            ),
        )
        if sess
        else Nav(
            A("Home", href="/"),
            A("Log In", href="/auth/login"),
        ),
        H1("Ay Gogh!"),
        sess and P(f"Hello {sess['name']}!"),
    )


def html_footer():
    return Footer(
        P(
            A("Ay Gogh!", href="/"),
            " was created with ❤️ by  ",
            A("huangphoux", href="https://github.com/Huangphoux/"),
            ".",
        )
    )
