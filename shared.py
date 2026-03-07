from starhtml import *
from db import DatabaseDict
from relay import Relay

db = DatabaseDict()
relay: Relay[str] = Relay()


def html_header(sess=None):
    return Header(
        Nav(
            A("Home", href="/"),
        ),
        H1("Ay Gogh!"),
    )


def html_footer():
    return Footer(
        P(
            "Ay Gogh! was created with ❤️ by  ",
            A("huangphoux", href="https://github.com/Huangphoux/"),
            ".",
        )
    )
