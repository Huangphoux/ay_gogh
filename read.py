import html

from starhtml import *
from fh_posts.all import *

from shared import theme_toggle, scroll_btn

from mistletoe import markdown
from mistletoe.html_renderer import HtmlRenderer

read_rt = APIRouter(prefix="/read")


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

    if content.startswith("---"):  # Remove frontmatter if present
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    # MD → HTML using AsideCodeRenderer
    html_content = str(markdown(content, AsideCodeRenderer))

    return NotStr(html_content)


def card(chpt):
    return A(
        Card(
            DivFullySpaced(
                H2(f"# {chpt.number}", cls="text-2xl"),
                H1(chpt.title, cls=("text-3xl text-right")),
                cls="space-x-4 h-full w-full",
            ),
            cls=("h-full", CardT.hover, f"hover:{CardT.primary}"),
        ),
        href=f"/read/{chpt.slug}",  # type: ignore
    )


@read_rt("/page")
def page(idx: int = 0):
    return load_chapter(idx)


def load_chapter(part_num: int = 1, size: int = 10):
    chapters = sorted(load_posts("test"), key=lambda chapter: chapter.number)

    # Calculate the start and end indices for this page
    start_idx = (part_num - 1) * size
    end_idx = start_idx + size

    # Only get the chapters for this page
    paginated = [card(chapter) for chapter in chapters[start_idx:end_idx]]

    # Add HTMX attributes to the last item
    if paginated:
        paginated[-1].attrs.update(
            {
                "hx-get": f"page?idx={part_num + 1}",
                "hx-trigger": "intersect",
                "hx-swap": "afterend",
            }
        )

    return paginated


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


@read_rt("/")
def index():
    return (
        Title("Ay Gogh !"),
        Main(cls="md:max-w-xl mx-auto px-4 py-8")(
            Header(
                navbar,
                DividerSplit(),
                theme_toggle,
            ),
            DivVStacked(cls="space-y-4 p-5 items-stretch")(
                *load_chapter(1),
            ),
            scroll_btn,
        ),
        Footer(),
    )


@read_rt("/{slug}")
def read_chpt(slug: str):
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
            scroll_btn,
            Article(content, cls="text-justify "),
            DivFullySpaced(
                A("← Previous Chapter", href=f"/chapter/{int(slug) - 1}", cls="mt-10"),
                A("Next Chapter →", href=f"/chapter/{int(slug) + 1}", cls="mt-10"),
            ),
            cls="md:max-w-xl mx-auto px-4 py-8",  # Added w-full
        ),
    )
