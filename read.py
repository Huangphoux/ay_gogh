import simplemma
from load_env import is_debug
from test import get_last_test
from apswutils.db import NotFoundError
from starhtml import *
from shared import db, relay, template
import mistletoe
from math import ceil
from mistletoe.html_renderer import HtmlRenderer
import re
from popup import popup_view
from math import floor

rt: APIRouter = APIRouter("/read")


def get_ease(score: int, ngsl: float):
    ease = score * ngsl

    if ease > 90:
        return "easy"

    if 80 <= ease <= 90:
        return "medium"

    if ease < 80:  # why did i write 80 < ease :'(
        return "hard"


@rt.get("/")
def read(auth, p: int = 0, all: int = 0):
    if p not in (0, 1, 2, 3, 4, 5) or all not in (0, 1):
        return Redirect("/read")

    if all:
        chap = db.app.query("SELECT number, title, ngsl FROM chapter")
    else:
        chap = db.app.query(
            "SELECT number, title, ngsl FROM chapter LIMIT 10 OFFSET ?", (p * 10,)
        )

    chap = list(chap)

    chap_done = list(
        db.get(auth).query("SELECT number FROM chapter WHERE done IS NOT NULL")
    )
    completed_numbers = {c["number"] for c in chap_done}

    for c in chap:
        c["done"] = c["number"] in completed_numbers

    last_test = get_last_test(auth)
    result = last_test["result"] if last_test else None
    progress = last_test["progress"] if last_test else None

    if not all:
        h1 = H1(
            id="main-heading",
            style=f"view-transition-name: read",
        )(f"Read, {p * 10 + 1} to {(p + 1) * 10}")

        pagination = Div(
            style="display: flex; gap: 1rem; align-items: center; height: 1.5rem"
        )(
            # Previous
            A(href=f"/read/?p={p - 1}")("Previous")
            if p > 0
            else Span(style="color: var(--border)")("Previous"),
            # Page numbers
            *(
                A(href=f"/read/?p={i}")(i)
                if i != p
                else Span(
                    style="font-style: italic; font-weight: bold; font-size: 3rem"
                )(i)
                for i in range(0, 6)
            ),
            # Next
            A(href=f"/read/?p={p + 1}")("Next")
            if p < 5
            else Span(style="color: var(--border)")("Next"),
        )

        show_all = A(href="/read/?all=1")("Show all")

    else:
        h1 = H1(
            id="main-heading",
            style=f"view-transition-name: read",
        )(f"Read All")
        pagination = None
        show_all = A(href="/read/?all=0")("Show less")

    chapters = Ul(style="padding: 0;")(
        *(
            Li(style="display: flex; justify-content: space-between;")(
                # Chapter {number}: {title}
                Span(
                    Span(style=f"view-transition-name: num{c['number']}")(
                        f"Chapter {c['number']:02}: "
                    ),
                    A(
                        href=f"/read/{c['number']}",
                        style=f"view-transition-name: chap{c['number']}"
                        if not c["done"]
                        else f"color: var(--border); view-transition-name: done{c['number']}",
                    )(f"{c['title']}", " (DONE)" if c["done"] else ""),
                ),
                # Reading ease difficulty: Easy, Medium, Hard
                A(
                    style=f"display: grid; place-items: center; view-transition-name: ease{c['number']};"
                )(
                    _class=(ease := get_ease(result, c["ngsl"])),
                    href=f"/read/{c['number']}/ease",
                )(ease.title())
                if result is not None and progress == 100 and not c["done"]
                else None,
            )
            for c in chap
        ),
    )

    flex = Div(
        Style("""
            me {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                flex-direction: column;
                
                @media md {
                    flex-direction: row;
                }
            }
        """),
        pagination,
        search_box(),
    )

    main = Main(h1, flex, chapters, show_all)

    return template(
        f"Read, {p * 10 + 1} to {(p + 1) * 10}" if not all else "Read All", main, auth
    )


def search_box(q: str = ""):
    return Search(
        Style("""
            me {
                position: sticky;
                top: 0;
                background-color: var(--bg);
            }
        """),
        Form(action="/read/search")(
            Label(_for="query")("Search for a word in every chapter"),
            Input(type="search", id="query", name="q", value=q),
            Button(type="submit")("Search"),
        ),
    )


@rt.get("/search")
def search(auth, q: str = ""):

    h1 = H1(id="main-heading")(f"Search in chapters")

    rows = (
        list(
            db.app.query(
                """
                SELECT DISTINCT number, snippet(chapter_search, -1, '<b>', '</b>', '...', 20) as Snippet
                FROM chapter_search(?)
                ORDER BY number
        """,
                (f'"{q}"',),
            )
        )
        if q
        else []
    )

    table = (
        Table(
            Thead(
                Tr(
                    Th(scope="col")("Chapter"),
                    Th(scope="col")("Snippets"),
                )
            ),
            Tbody(
                *(
                    Tr(
                        Th(scope="row")(
                            A(href=f"/read/{row['number']}")(f"Chapter {row['number']}")
                        ),
                        Td(Safe(row["Snippet"])),
                    )
                    for row in rows
                ),
            ),
        )
        if q
        else None
    )

    main = Main(h1, search_box(q), table)

    return template(f"Read, Search{f'for "{q}"' if q else ''}", auth=auth, main=main)


@rt.get("/{num:int}/ease")
async def ease(auth, num: int):
    if num not in range(1, 60 + 1):
        return Redirect("/read")

    chap = list(db.app.query("SELECT ngsl FROM chapter WHERE number = ? ", (num,)))[0]

    last_test = get_last_test(auth)

    if last_test:
        if last_test["progress"] != 100:
            return Redirect(f"/read/{num}")

        score = last_test["result"]
        ease = get_ease(score, chap["ngsl"])
    else:
        return Redirect(f"/read/{num}")

    h1 = H1(id="main-heading", style=f"view-transition-name: num{num}")(
        f"Chapter {num}: ",
        Span(_class=ease, style=f"view-transition-name: ease{num}")(ease.title()),
    )

    judgement = Section(
        Table(
            Thead(Tr(Th("Explanation"), Th("Percentage"))),
            Tbody(
                Tr(Td(f"NGSL words in chapter {num}"), Td(f"{chap['ngsl']:.2%}")),
                Tr(Td(f"NGSL words that you know"), Td(f"{score}%")),
                Tr(
                    Td(f"NGSL words that you know in chapter {num}"),
                    Td(_class=ease)(f"{score * chap['ngsl']:.2f}%"),
                ),
            ),
        ),
        P(
            "This chapter is deemed of ",
            Span(_class=ease)(ease.title()),
            " difficulty for you.",
        ),
        A(href=f"/read/{num}", _class="button")("Let's read!"),
    )

    reference = Section(
        P(
            "The table below refers to how difficult a chapter is \
                if you know a centain percentage of words in a chapter."
        ),
        P(
            "This information is taken from ",
            A(href="https://www.newgeneralservicelist.com/coverage")(
                "The Importance of Coverage in Vocabulary Learning"
            ),
            " by the New General Service List Project.",
        ),
        Table(
            Thead(Tr(Th("Percentage"), Th("Difficulty"))),
            Tbody(
                Tr(Td(f"≥ 90%"), Td(_class="easy")("Easy")),
                Tr(Td(f"80% < x < 90%"), Td(_class="medium")("Medium")),
                Tr(Td(f"≤ 80%"), Td(_class="hard")("Hard")),
            ),
        ),
    )

    main = Main(h1, judgement, reference)

    return template(f"Read, Chapter {num}'s reading ease", main, auth)


@rt.get("/{num:int}")
def chapter(auth, num: int, word: str = ""):
    if num not in range(1, 60 + 1):
        return Redirect("/read")

    return template(
        f"Read, Chapter {num}", auth=auth, main=chapter_main(auth, num, word)
    )


@rt.get("/{num:int}/cqrs")
@sse
async def cqrs(req, auth, num: int):
    async for _, data in relay.subscribe(f"read.{auth}.{num}"):
        yield elements(
            chapter_main(
                auth,
                num,
                word=data["word"],
                bypass=data["bypass"],
                context=data["context"],
            ),
            selector="main",
            use_view_transition=True,
        )


def show_popup(num: int, is_click: bool = False):
    get_clicked_word: str = "$word = evt.target.textContent;"

    code = f"""
            if ($word !== \"\" ) {{
                @get('/read/{num}/open');\
                document.querySelector('#popup').showPopover();
            }};
        """

    return js((get_clicked_word if is_click else "") + code)


def mark_word(num: int, content: str, card: dict) -> str:
    is_code: bool = False

    for i, line in enumerate(split := (content.splitlines())):
        if line == "```":
            is_code = not is_code
        if is_code:
            continue

        tokens = simplemma.simple_tokenizer(line)
        lemmas = simplemma.text_lemmatizer(line, lang="en")
        marked = []  # pass token if already marked

        for j, lemma in enumerate(lemmas):
            if card["front"] == lemma and tokens[j] not in marked:
                split[i] = re.sub(
                    r"\b%s\b" % tokens[j],
                    Safe(
                        Span(
                            data_is_retired=card["is_retired"],
                            data_is_new_day=card["is_new_day"],
                            data_is_due=card["is_due"],
                            data_attr_style=f"$colorblind && 'background: initial; text-decoration: underline;'",
                            data_on_pointerup=(show_popup(num, True), dict(stop=True)),
                            data_indicator="loading",
                        )(tokens[j])
                    ),
                    split[i],  # why can't i use `line` here?
                    # because using line doesn't modify the item in the list, dumbass
                )

                marked.append(tokens[j])

    return "\n".join(split)


def get_lines(num: int) -> list[str]:
    chap: str = db.app.item("SELECT content FROM chapter WHERE number = ? ", (num,))
    lines: list[str] = list(filter(None, chap.splitlines()))

    is_open: bool = False
    code_open: int = 0
    code_close: int = 0
    total_lines: int = len(lines)

    i = 0
    while i != total_lines:
        if not is_open and lines[i] == "```":
            is_open = True
            code_open = i
            i += 1
            continue

        if is_open and lines[i] == "```":
            is_open = False
            code_close = min(i + 1, total_lines)  # do not go over len(lines)

            # https://stackoverflow.com/a/1142879
            lines[code_open:code_close] = ["\n".join(lines[code_open:code_close])]
            total_lines = len(lines)

            i = code_open + 1
            continue

        i += 1

    return lines


def get_notes(num: int) -> list[str]:
    lines: list[str] = get_lines(num)
    return [line for line in lines if "```" in line]


def chapter_main(auth, num: int, word: str = "", bypass: int = 0, context: str = ""):
    # execute for INSERT, query for SELECT
    # this one is app
    chap = list(db.app.query("SELECT * FROM chapter WHERE number = ? ", (num,)))[0]

    try:
        progress: int = db.get(auth).item(
            "SELECT progress FROM chapter WHERE number = ? ", (num,)
        )
        is_done: bool = (
            db.get(auth).item("SELECT done FROM chapter WHERE number = ? ", (num,))
            is not None
        )
    except NotFoundError:
        progress: int = 1
        is_done: bool = False

    try:
        cards = list(  # this one find all cards
            db.get(auth).query(
                """
    SELECT
        front, back, due, last_review, is_retired,
        CASE WHEN datetime() > due THEN 1 ELSE 0 END AS is_due,
                -- datetime now is after due
        CASE WHEN (last_review IS NULL AND julianday('now') - julianday(due) < 1) THEN 0 ELSE 1 END AS is_new_day
                --  no last_review       &   it has been 24 hours
    FROM deck
                """
            ),
        )
    except IndexError:
        cards = None

    lines: list[str] = get_lines(num)

    if cards:
        for card in cards:  # mark mined words
            lines = [mark_word(num, line, card) for line in lines]

    total_lines = db.get(auth).item("SELECT lines FROM chapter WHERE number=?", (num,))
    if not total_lines:
        total_lines = len(lines)

    colorblind = db.get(auth).item(
        "SELECT value FROM settings WHERE setting = 'colorblind'"
    )

    colorblind_mode = Div(style="display: flex;", data_ignore_morph=True)(
        Input(
            data_signals=dict(colorblind=int(colorblind)),
            type="checkbox",
            id="colorblind",
            name="colorblind",
            data_bind="colorblind",
            data_on_change=patch(f"/read/{num}/save_toggles"),
        ),
        Label(_for="colorblind", style="flex-shrink: 0; padding-left: 0.5rem")(
            "Colorblind mode"
        ),
    )

    cardinal = Section(
        Style("""
                me {
                    padding: 0;
                    margin: 0;
                    gap: 1rem;
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                }
        """),
        P(f"Chapter {chap['number_word']} ({num})"),
        P(f"The {chap['cardinal_word']} ({chap['cardinal']}) Chapter"),
    )

    h1 = H1(
        id="main-heading",
        style=f"display: grid; place-items: center; text-align: center; grid-auto-flow: row;",
    )(
        f"{chap['title']}",
        Span("(DONE)") if is_done else None,
    )

    complete_msg = (
        (
            P(_class="notice")("You have completed this chapter."),
            Div(style="display: flex; justify-content: space-between;")(
                A(href=f"/read/{num - 1}")(f"Chapter {num - 1}"),
                A(href=f"/read/?p={ceil(num / 10) - 1}")("Back to List"),
                A(href=f"/read/{num + 1}")(f"Chapter {num + 1}"),
            ),
        )
        if is_done
        else None
    )

    show_all_notes = (
        Button(popovertarget="popup_notes", _class="outline")("Show all notes"),
        Dialog(
            popover=True,
            id="popup_notes",
            style="width: 100%; height: 80%; overflow: auto;",
        )(
            Safe(mistletoe.markdown("\n".join(get_notes(num)), HtmlRenderer)),
            Button(
                popovertarget="popup_notes",
                popovertargetaction="hide",
                style="position: sticky; bottom: 0;",
            )("Close"),
        ),
    )

    scroll_btm = js("""
        const content = document.querySelector("section[data-indicator]");
        content.scrollBy({left: 0, top: content.scrollHeight, behavior: "instant",});
    """)

    due_card_state = ('data-is-due="1"', 'data-is-new-day="1"', 'data-is-retired="0"')

    if not is_done:
        if progress != total_lines:
            next_line = Button(
                data_on_click=(js(f"@patch('/read/{num}'); {scroll_btm}"),),
                disabled=all(state in lines[progress] for state in due_card_state),
            )("Advance")
        else:
            next_line = (
                Script(
                    src="https://cdn.jsdelivr.net/npm/@hiseb/confetti@2.1.0/dist/confetti.min.js"
                ),
                Button(
                    data_on_click=(
                        js(f"""
                        @patch('/read/{num}'); {scroll_btm}
                        
                        let positionList = [
                            {{ x: window.innerWidth * 0.50, y: window.innerHeight * 0.60 }},
                            {{ x: window.innerWidth * 0.25, y: window.innerHeight * 0.40 }},
                            {{ x: window.innerWidth * 0.75, y: window.innerHeight * 0.30 }},
                        ];
                        
                        for(let i = 0; i < positionList.length; i++) {{
                            setTimeout(() => confetti({{ position: positionList[i] }}), i * 250);
                        }}
                    """),
                    )
                )("Mark Complete"),
            )
    else:
        next_line = None

    content = Section(
        style="margin:0; min-height: 20rlh; height: 20rlh; overflow: auto;",
        data_indicator="loading",
        data_init=scroll_btm,
        data_on_pointerup=show_popup(num),
        data_on_selectionchange=(
            js("""
               let sel = document.getSelection();
               $word = sel.toString().trim();
               $context = sel.anchorNode.parentNode.textContent;
            """),
            dict(document=True),
        ),
    )(
        Style("""
            :is([data-is-new-day], [data-is-due], [data-is-due], [data-is-retired]) {
                color: light-dark(var(--text), var(--bg));
                user-select: none;
                cursor: pointer;
            }
            
            [data-is-due="1"] { background: red; }
            [data-is-due="0"] { background: lime; }
            [data-is-new-day="0"] { background: gold; } /* If not new day yet then doesn't matter due or not */
            [data-is-retired="1"] { background: aqua; } /* Retire mean no review, so don't show any other color */
        """),
        Safe(mistletoe.markdown("\n\n".join(lines[0:progress]), HtmlRenderer)),
    )  # text section

    due_cards = (
        [c for c in cards if c["is_due"] and c["is_new_day"] and not c["is_retired"]]
        if cards
        else None
    )

    retired_cards = [c for c in cards if c["is_retired"]] if cards else None

    before_complete = (
        Section(
            Details(
                Summary("Due words"),
                Ul(
                    *(
                        Li(
                            style="user-select: none; cursor: pointer;",
                            data_on_click=show_popup(num, True),
                        )(c["front"])
                        for c in due_cards
                    )
                ),
            )
        )
        if due_cards
        else None,
        Section(
            Details(
                Summary("Retired words"),
                Ul(
                    *(
                        Li(
                            style="user-select: none; cursor: pointer;",
                            data_on_click=show_popup(num, True),
                        )(c["front"])
                        for c in retired_cards
                    )
                ),
            )
        )
        if retired_cards
        else None,
    )

    debug_signals = (
        Details(data_ignore_morph=True)(
            Summary("Panel for debugging signals"),
            Pre(data_json_signals=True),
        )
        if is_debug
        else None
    )

    popup_btn = Button(
        _class="outline",
        data_on_click="document.querySelector('#popup').togglePopover();",
    )("Toggle popup")

    progress_bar = (
        Progress(id="lines", max=total_lines, value=progress)(
            f"{progress / total_lines:.2%}"
        )
        if not is_done
        else None
    )

    return Main(data_init=get(url=f"/read/{num}/cqrs"))(
        cardinal,
        h1,
        progress_bar,
        popup_view(auth, num, word, bypass, context),
        content,
        colorblind_mode,
        Div(
            Style("""
                me {
                    display: flex;
                    flex-direction: column;
                    
                    & > * {
                        flex: 1;
                    }
                    
                    @media sm {
                        flex-direction: row;
                        gap: 1rem;
                    }
                }
            """),
            show_all_notes,
            next_line,
            popup_btn,
        ),
        complete_msg,
        before_complete,
        debug_signals,
    )


def publish(auth, num: int, word: str = "", bypass: int = 0, context: str = ""):
    # pointerup→open()→cqrs()→popup_view()
    relay.publish(f"read.{auth}.{num}", dict(word=word, bypass=bypass, context=context))


@rt.patch("/{num:int}/save_toggles")
def save_toggles(auth, num: int, colorblind: int):
    db.get(auth).execute(
        "UPDATE settings SET value=? WHERE setting=?",
        (colorblind, "colorblind"),
    )
    publish(auth, num)


@rt.patch("/{num:int}")
def next_line(auth, num: int):
    lines: list[str] = get_lines(num)

    progress: int = db.get(auth).item(
        "SELECT progress FROM chapter WHERE number=? ", (num,)
    )

    db.get(auth).execute(
        "UPDATE chapter SET lines=?, progress=? WHERE number=?",
        (len(lines), progress + 1, num),
    )

    if progress >= len(lines):
        db.get(auth).execute(
            "UPDATE chapter SET done=CURRENT_DATE WHERE number=?",
            (num,),
        )

        update_streak(auth)

    publish(auth, num)


def get_days_since_last_date(auth) -> int:
    return floor(
        db.get(auth).item(
            "SELECT JULIANDAY('now') - JULIANDAY(value) FROM settings WHERE setting=?",
            ("last_date",),
        )
    )


def update_streak(auth):
    # Julian day number: The number of days including fractional days
    # this function runs after user have done reading a book

    days_since_last_date: int = get_days_since_last_date(auth)

    num_book_done: int = db.get(auth).item("SELECT COUNT(done) FROM chapter")

    # first day finish a book, or next day finish a book
    if days_since_last_date == 0 and num_book_done == 1 or days_since_last_date == 1:
        db.get(auth).execute(
            "UPDATE settings SET value=value+1 WHERE setting=?", ("streak",)
        )

    # finish a book after a while, or first day not read
    if days_since_last_date > 1:
        db.get(auth).execute("UPDATE settings SET value=1 WHERE setting=?", ("streak",))

    db.get(auth).execute(
        "UPDATE settings SET value=CURRENT_DATE WHERE setting=?", ("last_date",)
    )
