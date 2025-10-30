import html
from fasthtml.common import *
from monsterui.all import *
from fh_posts.all import *

from mistletoe import markdown
from mistletoe.html_renderer import HtmlRenderer


class AsideCodeRenderer(HtmlRenderer):
    def render_block_code(self, token):
        template = "<aside{attr}><pre>{inner}</pre></aside>"
        base_class = (
            "block float-none m-10 "  # mobile-first
            "lg:relative lg:inline lg:float-right lg:-mr-[20vw] "
            "[&:nth-of-type(odd)]:lg:float-left [&:nth-of-type(odd)]:lg:-ml-[20vw]"
        )
        if token.language:
            lang_class = "language-{}".format(html.escape(token.language))
            attr = ' class="{} {}"'.format(base_class, lang_class)
        else:
            attr = ' class="{}"'.format(base_class)
        inner = self.escape_html_text(token.content)
        return template.format(attr=attr, inner=inner)


def render_md_aside(post):
    """Render a Markdown post using AsideCodeRenderer."""

    with open(post.path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove frontmatter if present
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    # Convert entire markdown to HTML using AsideCodeRenderer
    html_content = str(markdown(content, AsideCodeRenderer))

    return NotStr(html_content)


hdrs = (
    Theme.violet.headers(
        radii=ThemeRadii.lg,
        shadows=ThemeShadows.md,
        font=ThemeFont.default,
    ),
    Link(rel="icon", href="https://fav.farm/🔥"),
    Script(src="https://unpkg.com/hyperscript.org@0.9.14", defer=""),
    Style("""
        .dark .sun-icon { display: inline; }
        .dark .moon-icon { display: none; }
        html:not(.dark) .sun-icon { display: none; }
        html:not(.dark) .moon-icon { display: inline; }
    """),
)


app, rt = fast_app(hdrs=hdrs)

navbar_icon_size = 30

top_icons = [
    ("book-open", "Read !"),
    ("layers", "Review !"),
    ("bot-message-square", "Ask !"),
]
navbar = NavBar(
    *[
        UkIcon(
            icon[0],
            uk_tooltip=icon[1],
            height=navbar_icon_size,
            width=navbar_icon_size,
        )
        for icon in top_icons
    ],
    DiceBearAvatar("Easton", h=10, w=10),
    brand=DivLAligned(
        UkIconLink("book-check", height=20, width=20),
        H3("Ay Gogh !"),
    ),
)


def chapter_card(chapter):
    """Creates a card for a chapter preview"""

    return A(
        Card(
            DivFullySpaced(
                H2(f"# {chapter.number}", cls="text-2xl"),
                H1(chapter.title, cls=("text-3xl text-right")),
                cls="space-x-4 h-full w-full",
            ),
            cls=("h-full", CardT.hover),
        ),
        href=f"/chapter/{chapter.slug}",
    )


@rt
def page(idx: int = 0):
    return load_chapter(idx)


def load_chapter(part_num: int = 1, size: int = 10):
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
                "hx-trigger": "load",
                "hx-swap": "afterend",
            }
        )

    return paginated


theme_toggle = Button(
    UkIcon("sun", height=24, width=24, cls="sun-icon"),
    UkIcon("moon", height=24, width=24, cls="moon-icon"),
    _="on click toggle .dark on <html/>",
    cls=("fixed bottom-10 left-10 z-50 p-4", ButtonT.secondary),
)


@rt
def index():
    return (
        Title("Ay Gogh !"),
        Main(
            Header(
                navbar,
                DividerSplit(),
                theme_toggle,
            ),
            DivVStacked(
                *load_chapter(1),
                cls="space-y-4 p-5 items-stretch",
            ),
            cls="md:max-w-xl mx-auto px-4 py-8",
        ),
        Footer(),
    )


scroll_top_bottom_btn = (
    DivVStacked(
        Button(
            "↑",
            _="on click go to top of the body smoothly",
            cls=("text-2xl p-5", ButtonT.secondary),
        ),
        Button(
            "↓",
            _="on click go to bottom of the body smoothly",
            cls=("text-2xl p-5", ButtonT.secondary),
        ),
        cls="space-y-4 fixed bottom-10 right-10 z-50",
    ),
)


@rt("/chapter/{slug}")
def get(slug: str):
    chapters = load_posts("test")

    chapter = next((ch for ch in chapters if ch.slug == slug), None)
    if not chapter:
        return Titled(
            "404, we're so sorry !",
            P(
                "It's a shame that we can't find the chapter that you requested anywhere"
            ),
        )

    content = render_md_aside(chapter)

    chapter_str = f"Chapter {chapter.number_word} ({chapter.number})"
    the_chapter_str = f"The {chapter.cardinal_word} ({chapter.cardinal_number}) Chapter"

    return (
        Title(f"{chapter.title} - Ay Gogh !"),
        Main(cls="uk-container mt-5")(
            Header(
                DivVStacked(
                    A("← Back to Home", href="/", cls="mb-10"),
                    H2(chapter_str, cls="text-3xl text-center"),
                    H2(the_chapter_str, cls="text-3xl text-center"),
                    H1(chapter.title, cls="text-7xl text-center"),
                    P(chapter.reading_time, cls=TextPresets.muted_sm),
                    cls="space-y-4",  # Ensure inner content respects container width
                ),
                Divider(cls="my-10"),
                theme_toggle,
            ),
            scroll_top_bottom_btn,
            Article(content, cls="text-justify "),
            DivFullySpaced(
                A("← Previous Chapter", href=f"/chapter/{int(slug) - 1}", cls="mt-10"),
                A("Next Chapter →", href=f"/chapter/{int(slug) + 1}", cls="mt-10"),
            ),
            cls="md:max-w-xl mx-auto px-4 py-8",  # Added w-full
        ),
    )


serve()
