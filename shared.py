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

    header = Header(
        nav,
        H1("Ay Gogh!"),
        Noscript(P("JavaScript is needed to ensure the best experience.")),
    )

    footer = Footer(
        auth
        and Button(
            data_on_pointerdown=js("confirm('Are you SURE you want to sign out?')").if_(
                delete("/auth/login"), ""
            )
        )("Log Out"),
        P(
            A(href="https://github.com/Huangphoux/ay_gogh/")("Ay Gogh!"),
            " is created ",
            A(href="https://github.com/Huangphoux/")("huangphoux"),
            " and all of his ❤️. Copyright © Ay Gogh! 2026.",
        ),
        P(
            "Powered by ",
            A(href="https://data-star.dev/")("Datastar"),
            " 🚀 and ",
            A(href="https://starhtml.com/")("StarHTML"),
            " ⭐",
        ),
    )

    return (
        Title(f"{title}: Ay Gogh!"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            header,
            main,
            footer,
        ),
    )


# Starlette validates if the arg is in the request
# If not or invalid, fail before reaching the function
