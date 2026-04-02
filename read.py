from starhtml import *
from shared import db, html_header, html_footer, relay
import mistletoe


read_rt: APIRouter = APIRouter("/read")


@read_rt.get("/")
def read(sess, p: int = 0, all: int = 0):
    if p < 0 or p > 5 or all not in (0, 1):
        return Redirect("/")

    if not all:
        chap = list(db.app.query("SELECT * FROM chapter LIMIT 10 OFFSET ?", (p * 10,)))
        user_chap = list(
            db.get(sess["name"]).query(
                "SELECT * FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
            )
        )
    else:
        chap = list(db.app.query("SELECT * FROM chapter"))
        user_chap = list(db.get(sess["name"]).query("SELECT * FROM chapter"))

    chap = [a | b for a, b in zip(chap, user_chap)]

    return (
        Title(
            f"Read, {p * 10 + 1} to {(p + 1) * 10}: Ay Gogh"
            if not all
            else "Read All: Ay Gogh"
        ),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1(id="main-heading")(
                    f"Read (Chapter {p * 10 + 1} to {(p + 1) * 10})"
                    if not all
                    else "Read All",
                ),
                Div(
                    style="display: flex; gap: 1rem; align-items: center; height: 1.5rem"
                )(
                    A(href=f"/read?p={p - 1}")("Previous")
                    if not all and p > 0
                    else Span(style="color: var(--border)")("Previous"),
                    *(
                        A(href=f"/read?p={i}")(i)
                        if i != p
                        else Span(
                            style="font-style: italic; font-weight: bold; font-size: 3rem"
                        )(i)
                        for i in range(0, 6)
                    ),
                    A(
                        href=f"/read?p={p + 1}",
                    )("Next")
                    if not all and p < 5
                    else Span(style="color: var(--border)")("Next"),
                )
                if not all
                else None,
                Ul(
                    *(
                        Li(
                            A(
                                href=f"/read/{c['number']}",
                                style="color: var(--border)"
                                if int(c["done"]) == 1
                                else None,
                            )(
                                f"Chapter {c['number']}: {c['title']}"
                                if int(c["done"]) == 0
                                else f"{c['number']} (DONE)",
                            ),
                        )
                        for c in chap
                    ),
                ),
                A(href="/read?all=1")("Show all")
                if not all
                else A(href="/read?all=0")("Show less"),
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
                A(href="/read?all=0")("Back"),
                Section(style="display: flex; justify-content: space-between")(
                    P(f"Chapter {chap['number_word']} ({num})"),
                    P(f"The {chap['cardinal_word']} ({chap['cardinal']}) Chapter"),
                ),
                H1(id="main-heading", style="display:grid; place-items: center")(
                    f"{chap['title']}",
                ),
                Section(
                    P(
                        Safe(
                            mistletoe.markdown(chap["content"]),
                        ),
                    ),
                ),
                A(href="/read?all=0")("Back"),
            ),
            html_footer(sess),
        ),
    )
