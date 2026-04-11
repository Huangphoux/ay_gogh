from starhtml import *
from shared import db, html_header, html_footer, relay
from fsrs import ReviewLog, Optimizer
from datetime import datetime, timezone

set_rt: APIRouter = APIRouter("/settings")


@set_rt.get("/")
def index(sess):
    return (
        Title(f"Settings: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Settings", id="main-heading"),
                Ul(
                    Li(A(href=fsrs)("FSRS")),
                    Li(A(href="/")("Reset Password")),
                ),
            ),
            html_footer(sess),
        ),
    )


@set_rt.get("/fsrs")
def fsrs(sess):
    return fsrs_view(sess)


@set_rt.get("/fsrs/cqrs")
@sse
async def fsrs_cqrs(req, sess):
    async for _, data in relay.subscribe(f"settings.{sess['name']}.fsrs"):
        yield elements(fsrs_view(sess, notif=data), use_view_transition=True)


def fsrs_view(sess, notif: str = ""):
    settings = list(
        db.get(sess["name"]).query(
            "SELECT setting, value FROM settings",
        ),
    )

    for s in settings:
        if s["setting"] == "desired_retention":
            desired_retention = s["value"]
        if s["setting"] == "parameters":
            parameters = [float(p.strip()) for p in s["value"].split(",")]

    return (
        Title(f"Settings, FSRS: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(data_init=get(fsrs_cqrs))(
                H1("FSRS", id="main-heading"),
                Form(
                    Label(_for="desired_retention")("Desired Retention (70-100)"),
                    Input(
                        id="desired_retention",
                        name="desired_retention",
                        value=int(float(desired_retention) * 100),
                        type="number",
                        max="100",
                        min="70",
                        required="True",
                        placeholder="e.g. 80",
                    ),
                    Button(
                        data_on_click=patch(
                            "/settings/fsrs/save", {"contentType": "form"}
                        )
                    )("Save"),
                    Label(_for="parameters")("Parameters (cannot modify)"),
                    Textarea(
                        id="parameters",
                        name="parameters",
                        style="resize: none;",
                    )(parameters),
                    Button(
                        data_on_click=patch(optimize),
                        data_indicator="optimizing",
                        data_attr_disabled="$optimizing",
                    )("Optimize"),
                ),
                P(_class="notice", data_show="$optimizing")("Optimizing…"),
                P(_class="notice")(notif) if notif else None,
            ),
            html_footer(sess),
        ),
    )


@set_rt.patch("/fsrs/save")
def save(sess, desired_retention: int):
    if not desired_retention:
        return Redirect("/")

    db.get(sess["name"]).execute(
        "UPDATE settings SET value=? WHERE setting=?",
        (desired_retention / 100, "desired_retention"),
    )

    relay.publish(
        f"settings.{sess['name']}.fsrs",
        "Your desired retention value has been updated.",
    )


@set_rt.patch("/fsrs/optimize")
def optimize(sess):
    query = list(
        db.get(sess["name"]).query(
            "SELECT * FROM review_log",
        ),
    )

    review_logs: list[ReviewLog] = [
        ReviewLog(
            card_id=q["card_id"],
            rating=q["rating"],
            review_datetime=datetime.strptime(
                q["review_datetime"], "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=timezone.utc),
            review_duration=q["review_duration"],
        )
        for q in query
    ]

    optimizer = Optimizer(review_logs=review_logs)

    optimal_parameters = optimizer.compute_optimal_parameters()  # ty:ignore[unresolved-attribute]

    print(optimal_parameters)
    
    db.get(sess["name"]).execute(
        "UPDATE settings SET value=? WHERE setting=?",
        (", ".join([str(p) for p in optimal_parameters]), "parameters"),
    )

    relay.publish(
        f"settings.{sess['name']}.fsrs", "Your parameters have been optimized."
    )
