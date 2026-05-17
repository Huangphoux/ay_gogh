from starhtml import *
from shared import db, is_signed_in, template
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

auth_rt: APIRouter = APIRouter("/auth")


@auth_rt.get("/login")
def login(req, sess):
    if is_signed_in(req, sess):
        return Redirect("/")

    main = Main(show_pwd := Signal("show_pwd", False))(
        H1("Log In", id="main-heading"),
        Form(method="post", action="/auth/login")(
            Fieldset(
                Label(B("Username"), _for="name"),
                Input(
                    id="name",
                    name="name",
                    placeholder="Enter Username",
                    required=True,
                    maxlength="100",
                    autofocus=True,
                    value="DEBUG",
                    autocomplete="on",
                ),
                Label(B("Password"), _for="name"),
                Input(
                    data_attr_type=show_pwd.if_("text", "password"),
                    type="password",
                    id="pwd",
                    name="pwd",
                    placeholder="Enter Password",
                    required=True,
                    minlength="8",
                    maxlength="100",
                    value="DEBUG_DEBUG_DEBUG",
                    autocomplete="on",
                ),
                Br(),
                Input(
                    id="show_pwd",
                    name="show_pwd",
                    type="checkbox",
                    data_bind=show_pwd,
                ),
                Label("Show Password", _for="show_pwd"),
            ),
            Button(type="submit")("Log In"),
            Span(f" or "),
            A("Sign Up", href="/auth/signup"),
        ),
    )

    return template("Log In", main, sess.get("auth", None))


@auth_rt.post("/login")
def login_process(sess, name: str, pwd: str):
    if len(name) > 100 or (len(pwd) > 100 or len(pwd) < 8):
        return Redirect("/auth/login")

    rows = list(db.app.query("SELECT name, pwd FROM user WHERE name=?", (name,)))

    if not rows:  # no user in DB
        return Redirect("/auth/login")

    u = rows[0]  # there should only be one account that match
    if not pwd_context.verify(pwd, u["pwd"]):
        return Redirect("/auth/login")

    sess["auth"] = u["name"]
    return Redirect("/")


@auth_rt.delete("/login")
def logout(sess):
    db.close(sess["auth"])

    del sess["auth"]

    return Redirect("/")


@auth_rt.get("/signup")
def signup(req, sess):
    if is_signed_in(req, sess):
        return Redirect("/")

    main = Main(
        H1("Sign Up", id="main-heading"),
        Form(method="post", action="/auth/signup")(
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
                    id="show_pwd", name="show_pwd", type="checkbox", data_bind="is_show"
                ),
                Label("Show Password", _for="show_pwd"),
            ),
            Button(type="submit")("Sign Up"),
            P(
                "Maybe you want to ",
                A("Log In", href="/auth/login"),
                " instead?",
            ),
        ),
    )

    return template("Sign Up", main, sess.get("auth", None))


@auth_rt.post("/signup")
def signup_process(sess, name: str, pwd: str):
    if len(name) > 100 or (len(pwd) > 100 or len(pwd) < 8):
        return Redirect("/auth/signup")

    if list(  # DB has that account
        db.app.query("SELECT 1 FROM user WHERE name=?", (name,))
    ):
        return Redirect("/auth/signup")

    db.app.execute(
        "INSERT INTO user (name, pwd) VALUES (?, ?)", (name, pwd_context.hash(pwd))
    )

    sess["auth"] = name
    return Redirect("/")
