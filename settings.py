from starhtml import *
from shared import db, relay, template
from fsrs import ReviewLog, Optimizer
from datetime import datetime, timezone

rt: APIRouter = APIRouter("/settings")


@rt.get("/")
def index(auth):
    main = Main(
        H1("Settings", id="main-heading"),
        Ul(
            Li(style="view-transition-name: fsrs")(A(href="/settings/fsrs")("FSRS")),
        ),
    )

    return template("Settings", main, auth)


@rt.get("/fsrs")
def fsrs(auth):
    return template("Settings, FSRS", fsrs_main(auth), auth)


@rt.get("/fsrs/cqrs")
@sse
async def fsrs_cqrs(req, auth):
    async for _, data in relay.subscribe(f"settings.{auth}.fsrs"):
        yield elements(
            fsrs_main(auth, notif=data["msg"]),
            selector="main",
            use_view_transition=True,
        )


def fsrs_main(auth, notif: str = ""):
    settings = list(db.get(auth).query("SELECT setting, value FROM settings"))

    for s in settings:
        if s["setting"] == "desired_retention":
            desired_retention = float(s["value"])
        if s["setting"] == "parameters":
            parameters = [float(p.strip()) for p in s["value"].split(",")]

    return Main(data_init=get("/settings/fsrs/cqrs"))(
        H1("FSRS", id="main-heading", style="view-transition-name: fsrs"),
        P(
            "FSRS, the Free Spaced Repetition Scheduling algorithm, \
                     is the backbone of the spaced retention aspect of this app."
        ),
        H2("Desired Retention"),
        P(
            "From the Anki manual:",
            Blockquote(
                cite="https://docs.ankiweb.net/deck-options.html#desired-retention"
            )(
                "Desired retention controls how likely you are to remember cards \
                            when they are scheduled for a review. The default value of 0.90 \
                            will schedule cards so you have a 90% chance of remembering them \
                            when they come up for review again. This should normally translate to \
                            remembering around 90% cards when they are reviewed, and only failing around 10%."
            ),
        ),
        Label(_for="desired_retention")("Desired Retention (70-100)"),
        Input(
            id="desired_retention",
            value=int(desired_retention * 100),
            type="number",
            max="100",
            min="70",
            required="True",
            placeholder="e.g. 80",
            data_bind="desired_retention",
        ),
        Button(data_on_click=patch("/settings/fsrs/save"))("Save"),
        P(_class="notice")(notif) if "retention" in notif else None,
        H2("Parameters"),
        P(
            "From the Anki manual:",
            Blockquote(
                cite="https://docs.ankiweb.net/deck-options.html#fsrs-parameters"
            )(
                "FSRS parameters affect how cards are scheduled. \
                Do not change the parameters manually or copy them from someone else. \
                The FSRS optimizer uses machine learning to learn your memory patterns and \
                find parameters that best fit your review history. To do this, the optimizer \
                requires several reviews to fine-tune the parameters. \
                There is no need to optimize your parameters frequently: once every month is sufficient."
            ),
        ),
        P("Parameters"),
        P(_class="notice")(parameters),
        Button(
            data_on_click=get("/settings/fsrs/optimize"),
            data_indicator="optimizing",
            data_attr_disabled="$optimizing",
        )("Optimize"),
        P(_class="notice", data_show="$optimizing", style="display: none")(
            "Computing optimal parameters for you. This won't be long, please standby."
        ),
        P(_class="notice", data_show="!$optimizing")(notif)
        if "parameter" in notif
        else None,
    )


def publish(auth, msg: str = ""):
    relay.publish(f"settings.{auth}.fsrs", dict(msg=msg))


@rt.patch("/fsrs/save")
def save(auth, desired_retention: int):
    if desired_retention not in range(70, 100):
        return Redirect("/settings/fsrs")

    db.get(auth).execute(
        "UPDATE settings SET value=? WHERE setting=?",
        (desired_retention / 100, "desired_retention"),
    )

    publish(auth, "Your desired retention has been updated.")


@rt.get("/fsrs/optimize")
async def optimize(auth):
    query = list(db.get(auth).query("SELECT * FROM review_log"))

    review_logs: list[ReviewLog] = [
        ReviewLog(
            card_id=int(q["card_id"]),
            rating=q["rating"],
            review_datetime=datetime.strptime(
                q["review_datetime"], "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=timezone.utc),
            review_duration=q["review_duration"],
        )
        for q in query
    ]

    optimal_parameters = Optimizer(review_logs=review_logs).compute_optimal_parameters()  # ty:ignore[unresolved-attribute]

    db.get(auth).execute(
        "UPDATE settings SET value=? WHERE setting=?",
        (", ".join([str(p) for p in optimal_parameters]), "parameters"),
    )

    publish(auth, "Your parameters have been optimized.")
