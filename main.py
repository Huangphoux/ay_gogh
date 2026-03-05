from shared import html_header, html_footer
from starhtml import *


def not_found(req, exc):
    return H1("There's no such page like that!")


def set_auth(req, sess):
    auth = req.scope["auth"] = sess.get("auth", None)
    if not auth:
        return Redirect(login)


auth_bware = Beforeware(
    set_auth,
    skip=[r"/favicon\.ico", r"/static/.*", r".*\.css", "/", "/login", "/login_process"],
)

app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    debug=True,
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
            (timestamp := Signal("timestamp", js("Date.now()"))),
            Pre(data_json_signals=True),
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
    return Redirect(index)

    if not name or not pwd:
        return login_redir
    try:
        u = users[name]
    except NotFoundError:
        u = users.insert(name=name, pwd=pwd)
    if not compare_digest(u.pwd.encode("utf-8"), pwd.encode("utf-8")):
        return login_redir
    sess["auth"] = u.name


@rt
def logout(sess):
    del sess["auth"]
    return RedirectResponse(index, status_code=303)


if __name__ == "__main__":
    serve(port=1984)
