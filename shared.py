from starhtml import *
from db import DatabaseDict
from relay import Relay


db = DatabaseDict()
relay: Relay[dict] = Relay()


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
        # (
        #     brand := Signal(
        #         "brand",
        #         ["Êy Gôgh!", "英語！", "エイ・ゴー！", "Eigo!", "/eigo/!", "𠲖姑！"],
        #     )
        # ),
        nav,
        H1(
            style="cursor: pointer; user-select: none;",
            # data_on_click="evt.target.textContent=\
                # $brand[Math.floor(Math.random()*$brand.length)]",
        )("Ay Gogh!"),
        Noscript(P("Enable JavaScript to ensure the best experience.")),
    )

    footer = Footer(
        auth
        and Button(
            data_on_pointerdown=js("confirm('Are you SURE you want to sign out?')").if_(
                delete("/auth/login"), ""
            )
        )("Log Out"),
        P(
            "© 2026 ",
            A(href="https://github.com/Huangphoux/")("huangphoux"),
            ". Licensed under ",
            A(href="https://osaasy.dev/")("O'Saasy License."),
        ),
        P(
            A(href="https://github.com/Huangphoux/ay_gogh")("Ay Gogh!"),
            " is developed with ❤️ using ",
            A(href="https://www.python.org/")("Python"),
            ", ",
            A(href="https://sqlite.org/index.html")("SQLite"),
            ", ",
            A(href="https://data-star.dev/")("Datastar"),
            ", ",
            A(href="https://simplecss.org/")("Simple.css"),
            ", and ",
            A(href="https://starhtml.com/")("StarHTML"),
            ".",
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
