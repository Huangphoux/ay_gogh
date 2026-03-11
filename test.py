from starhtml import *
from shared import db, html_header, html_footer

test_rt: APIRouter = APIRouter("/test")


@test_rt.get("/")
def test(sess):
    tests = list(db.get(sess["name"]).query("SELECT * FROM test"))
    header = ["day", "form", "progress", "lv1", "lv2", "lv3", "lv4", "lv5"]

    return (
        Title(f"Test: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Test", id="main-heading"),
                Figure(
                    Table(
                        Thead(Tr(Th(h.title()) for h in header)),
                        Tbody(*[Tr(*[Td(t[h]) for h in header]) for t in tests]),
                    ),
                ),
            ),
            html_footer(sess),
        ),
    )
