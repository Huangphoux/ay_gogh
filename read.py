from starhtml import *
from shared import db, html_header, html_footer, relay

read_rt: APIRouter = APIRouter("/read")


@read_rt.get("/")
def read(sess, p: int = 0):
    if p < 0 or p > 5:
        return Redirect("/")

    chap = list(db.app.query("SELECT * FROM chapter LIMIT 10 OFFSET ?", (p * 10,)))

    return (
        Title(f"Read, {p * 10 + 1} to {(p + 1) * 10}: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1(
                    f"Read (Chapter {p * 10 + 1} to {(p + 1) * 10})",
                    id="main-heading",
                ),
                A(href=f"/read?p={p - 1}")("Previous") if p > 0 else None,
                Span(" "),
                A(href=f"/read?p={p + 1}")("Next") if p < 5 else None,
                Ul(
                    *(
                        Li(
                            A(href=f"/read/{c['number']}")(
                                f"Chapter {c['number']}: {c['title']}"
                            ),
                        )
                        for c in chap
                    ),
                ),
            ),
            html_footer(sess),
        ),
    )


@read_rt.get("/{num:int}")
def chapter(sess, num: int):
    # execute for INSERT, query for SELECT
    chap = list(db.app.query("SELECT * FROM chapter WHERE number = ? ", (num,)))[0]

    return (
        Title(f"Read, Chapter {num}: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                Section(style="display: flex; justify-content: space-between")(
                    P(f"Chapter {chap['number_word']} ({num})"),
                    P(f"The {chap['cardinal_word']} ({chap['cardinal']}) Chapter"),
                ),
                H1(id="main-heading", style="display:grid; place-items: center")(
                    f"{chap['title']}",
                ),
                Section(
                    P(chap["content"]),
                ),
            ),
            html_footer(sess),
        ),
    )
