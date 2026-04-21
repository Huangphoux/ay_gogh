from starhtml import *
from db import DatabaseDict
from relay import Relay


db = DatabaseDict()
relay: Relay[str] = Relay()


def is_signed_in(req, sess):
    return True if sess.get("auth", None) else False


def template(title: str, main, auth=None):
    if not auth:
        nav = Nav(
            A("Home", href="/"),
            A("Log In", href="/auth/login/"),
        )
    else:
        nav = Nav(
            A("Profile", href="/"),
            A("Settings", href="/settings/"),
        )

    return (
        Title(f"{title}: Ay Gogh!"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            Header(
                nav,
                H1("Ay Gogh!"),
                Noscript(P("JavaScript is needed to ensure the best experience.")),
            ),
            main,
            Footer(
                auth
                and A(
                    "Log Out",
                    data_on_click=js("confirm('Are you sure?')").if_(
                        delete("/auth/login/"), ""
                    ),
                ),
                P(
                    A(href="https://github.com/Huangphoux/ay_gogh/")("Ay Gogh!"),
                    " is created by the ❤️ of  ",
                    A(href="https://github.com/Huangphoux/")("huangphoux"),
                    ".",
                ),
                P("Copyright © Ay Gogh! 2026"),
            ),
        ),
    )
