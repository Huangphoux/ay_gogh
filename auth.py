from starhtml import *
from shared import db, html_header, html_footer
from passlib.context import CryptContext


auth_rt: APIRouter = APIRouter("/auth")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def login_view():
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
                        placeholder="Enter Password",
                        required=True,
                        data_attr_type="$is_show ? 'text' : 'password'",
                    ),
                    Input(
                        "Show Password",
                        type="checkbox",
                        data_bind="is_show",
                    ),
                ),
                Button("Login"),
                Span(f" or "),
                A("Sign Up", href=login),
            ),
        ),
        html_footer(),
    )


@auth_rt.get("/login")
def login():
    return login_view()


@auth_rt.post("/login_process")
def login_process(name: str, pwd: str, sess):
    global db
    db_app = db.get()

    if not name or not pwd:
        return Redirect("/auth/login")

    rows = list(db_app.query("SELECT name, pwd FROM user WHERE name=?", (name,)))

    if not rows:
        db_app.execute(
            "INSERT OR REPLACE INTO user (name, pwd) VALUES (?, ?)",
            (name, pwd_context.hash(pwd)),
        )
        sess["name"] = name
        db.get(name)
        return Redirect("/profile")

    u = rows[0]
    if not pwd_context.verify(pwd, u["pwd"]):
        return Redirect("/auth/login")

    sess["name"] = u["name"]
    return Redirect("/profile")


@auth_rt.get("/logout")
def logout(sess):
    del sess["name"]
    return Redirect("/")
