from fasthtml.common import *
from monsterui.all import *
from fh_posts.all import *

hdrs = (
    Theme.violet.headers(),
    Link(rel="icon", href="https://fav.farm/🔥"),
    Script(src="https://unpkg.com/hyperscript.org@0.9.14", defer=""),
)


app, rt = fast_app(
    hdrs=hdrs,
    static_path="static",
    mode="light",
)

navbar_icon_size = 15

navbar = NavBar(
    UkIconLink(
        "book-open",
        height=20,
        width=20,
    ),
    UkIconLink(
        "layers",
        height=20,
        width=20,
    ),
    UkIconLink(
        "bot-message-square",
        height=20,
        width=20,
    ),
    DiceBearAvatar("Alyssa", h=10, w=10),
    brand=DivLAligned(
        UkIconLink(
            "book-check",
            height=20,
            width=20,
        ),
        H3("Ay Gogh !"),
    ),
)


def chapter_card(chapter):
    """Creates a card for a chapter preview"""

    chapter_str = f"Chapter {chapter.number_word} ({chapter.number})"
    the_chapter_str = f"The {chapter.cardinal_word} ({chapter.cardinal_number}) Chapter"

    return A(
        Card(
            DivVStacked(
                H2(
                    f"{chapter_str} — {the_chapter_str}",
                    cls=TextPresets.muted_sm,
                ),
                H1(chapter.title, cls=("text-3xl")),
                P(chapter.reading_time, cls=TextPresets.muted_sm),
                cls="space-y-2 h-full",
            ),
            cls=("h-full", CardT.hover),
        ),
        href=f"/chapter/{chapter.slug}",
    )


@rt
def page(idx: int = 0):
    return generate_part(idx)


def generate_part(part_num: int = 1, size: int = 10):
    chapters = sorted(load_posts("test"), key=lambda chapter: chapter.number)

    # Calculate the start and end indices for this page
    start_idx = (part_num - 1) * size
    end_idx = start_idx + size

    # Only get the chapters for this page
    paginated = [chapter_card(chapter) for chapter in chapters[start_idx:end_idx]]

    # Add HTMX attributes to the last item
    if paginated:
        paginated[-1].attrs.update(
            {
                "hx-get": f"page?idx={part_num + 1}",
                "hx-trigger": "revealed",
                "hx-swap": "afterend",
            }
        )

    return paginated


@rt
def index():
    return (
        Title("Ay Gogh !"),
        Main(
            (navbar, DividerSplit()),
            DivVStacked(
                *generate_part(1),
                cls="space-y-4 p-5 items-stretch",
            ),
            cls="max-w-xl mx-auto px-4 py-8",
        ),
        Footer(),
    )


@rt("/chapter/{slug}")
def get(slug: str):
    chapters = load_posts("test")

    chapter = next((ch for ch in chapters if ch.slug == slug), None)
    if not chapter:
        return Titled("404, we're so sorry !")

    content = chapter.render()

    chapter_str = f"Chapter {chapter.number_word} ({chapter.number})"
    the_chapter_str = f"The {chapter.cardinal_word} ({chapter.cardinal_number}) Chapter"

    return (
        Title(f"{chapter.title} - Ay Gogh !"),
        Container(
            DivVStacked(
                A("← Back to Home", href="/", cls="mb-10"),
                H2(chapter_str, cls="text-3xl"),
                H2(the_chapter_str, cls="text-3xl"),
                H1(chapter.title, cls="text-7xl"),
                P(chapter.reading_time, cls=TextPresets.muted_sm),
                cls="space-y-4",  # Ensure inner content respects container width
            ),
            Divider(cls="my-10"),
            Button(
                "↑ Scroll to Top",
                _="on click go to top of the body smoothly",
                cls=f"fixed bottom-10 right-10 px-4 py-2 z-50 {ButtonT.primary}",
            ),
            Article(content),
            cls="max-w-xl px-4 py-8",  # Added w-full
        ),
    )


serve()
