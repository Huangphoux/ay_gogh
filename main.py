from shared import html_header, html_footer
from starhtml import *
from db import DatabaseDict
from relay import Relay
from hmac import compare_digest

db = DatabaseDict()
relay: Relay[str] = Relay()


def not_found(req, exc):
    return H1("There's no such page like that!")


def set_auth(req, sess):
    auth = req.scope["name"] = sess.get("name", None)
    if not auth:
        return Redirect(login)


auth_bware = Beforeware(
    set_auth,
    skip=[r"/favicon\.ico", r"/static/.*", r".*\.css", "/", "/login", "/login_process"],
)

app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={404: not_found},
    middleware=(compression(),),
    static_path="static",
    hdrs=(
        Link(rel="stylesheet", href="simple.min.css"),
        Link(rel="stylesheet", href="custom.css"),
    ),
    sess_https_only=False,  # secure
    same_site="strict",
)


@rt
def index():
    return (
        html_header(),
        Main(
            P("This page is in construction.", _class="notice"),
            A("Get started", href=login, _class="button"),
        ),
        html_footer(),
    )


@rt
def login():
    return Body(
        html_header(),
        Main(
            H1("Login"),
            Form(action=login_process, method="post")(
                Fieldset(
                    Label("Username", _for="name"),
                    Input(
                        id="name",
                        name="name",
                        placeholder="Enter Username",
                        required=True,
                    ),
                    Label("Password", _for="name"),
                    Input(
                        id="pwd",
                        name="pwd",
                        type="password",
                        placeholder="Enter Password",
                        required=True,
                    ),
                ),
                Button("Login"),
            ),
        ),
        html_footer(),
    )


@rt
def login_process(name: str, pwd: str, sess):
    global db
    db_app = db.get()

    if not name or not pwd:
        return Redirect(login)

    # query() returns generator
    rows = list(db_app.query("SELECT name, pwd FROM users WHERE name=?", (name,)))
    if not rows:
        db_app.execute(
            "INSERT OR REPLACE INTO users (name, pwd) VALUES (?, ?)", (name, pwd)
        )
        sess["name"] = name
        return Redirect(index)

    u = rows[0]
    if not compare_digest(u["pwd"].encode("utf-8"), pwd.encode("utf-8")):
        return Redirect(login)

    sess["name"] = u["name"]
    return Redirect(index)


@rt
def logout(sess):
    del sess["name"]
    return RedirectResponse(index, status_code=303)


if __name__ == "__main__":
    serve(port=1984)
