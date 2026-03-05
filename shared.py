from starhtml import *


def html_header():
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
