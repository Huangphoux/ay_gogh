from starhtml import *
from shared import db, is_signed_in, template
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

auth_rt: APIRouter = APIRouter("/auth")


@auth_rt.get("/login")
def login(req, sess):
    if is_signed_in(req, sess):
        return Redirect("/")

    main = Main(
        H1("Log In", id="main-heading"),
        Form(action=login_process, method="post")(
            Fieldset(
                Label(B("Username"), _for="name"),
                Input(
                    id="name",
                    name="name",
                    placeholder="Enter Username",
                    required=True,
                    maxlength="100",
                    autofocus=True,
                    onfocus="let temp=this.value; this.value=''; this.value=temp",
                    value="DEBUG",  ### DEBUG
                ),
                Label(B("Password"), _for="name"),
                Input(
                    data_attr_type="$is_show ? 'text' : 'password'",
                    type="password",
                    id="pwd",
                    name="pwd",
                    placeholder="Enter Password",
                    required=True,
                    minlength="8",
                    maxlength="100",
                    value="DEBUG",  ### DEBUG
                ),
                Br(),
                Input(
                    id="show_pwd",
                    name="show_pwd",
                    type="checkbox",
                    data_bind="is_show",
                    _class="no-js",
                ),
                Label("Show Password", _for="show_pwd", _class="no-js"),
            ),
            Button("Log In"),
            Span(f" or "),
            A("Sign Up", href=signup),
        ),
    )

    return template("Log In", main, sess.get("auth", None))


@auth_rt.post("/login")
def login_process(name: str, pwd: str, sess):
    if not name or not pwd:
        return Redirect(login)

    global db
    rows = list(db.app.query("SELECT name, pwd FROM user WHERE name=?", (name,)))

    if not rows:
        return Redirect(login)

    u = rows[0]
    if not pwd_context.verify(pwd, u["pwd"]):
        return Redirect(login)

    sess["auth"] = u["name"]
    return Redirect("/")


# @auth_rt.delete("/logout")
@auth_rt.post("/logout")
def logout(sess):
    global db
    db.close(sess["auth"])

    del sess["auth"]

    return Redirect("/")


@auth_rt.get("/signup")
def signup(req, sess):
    if is_signed_in(req, sess):
        return Redirect("/")

    main = Main(
        H1("Sign Up", id="main-heading"),
        Form(action=signup_process, method="post")(
            Fieldset(
                Label(B("Username *"), _for="name"),
                Input(
                    id="name",
                    name="name",
                    placeholder="Enter Username",
                    required=True,
                    maxlength="100",
                    autofocus=True,
                    onfocus="let temp=this.value; this.value=''; this.value=temp",
                ),
                Label(B("Password *"), _for="name"),
                Input(
                    data_attr_type="$is_show ? 'text' : 'password'",
                    type="password",
                    id="pwd",
                    name="pwd",
                    placeholder="Enter Password",
                    required=True,
                    minlength="8",
                    maxlength="100",
                ),
                Br(),
                Input(
                    id="show_pwd",
                    name="show_pwd",
                    type="checkbox",
                    data_bind="is_show",
                    _class="no-js",
                ),
                Label(
                    "Show Password",
                    _for="show_pwd",
                    _class="no-js",
                ),
            ),
            Button("Sign Up"),
            P(
                "Maybe you want to ",
                A("Log In", href=login),
                " instead?",
            ),
        ),
    )

    return template("Sign Up", main, sess.get("auth", None))


@auth_rt.post("/signup")
def signup_process(name: str, pwd: str, sess):
    if not name or not pwd:
        return Redirect(login)

    global db
    rows = list(db.app.query("SELECT 1 FROM user WHERE name=?", (name,)))

    if rows:  # there's already someone with that name
        return Redirect(signup)

    db.app.execute(
        "INSERT INTO user (name, pwd) VALUES (?, ?)",
        (name, pwd_context.hash(pwd)),
    )

    sess["auth"] = name
    return Redirect("/")
