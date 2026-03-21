from starhtml import *
from shared import db, html_header, html_footer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

auth_rt: APIRouter = APIRouter("/auth")


@auth_rt.get("/login")
def login():
    return (
        Title(f"Login: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(),
            Main(
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
                            value="asd",  ### DEBUG
                        ),
                        Label(B("Password"), _for="name"),
                        Input(
                            data_attr_type="$is_show ? 'text' : 'password'",
                            id="pwd",
                            name="pwd",
                            placeholder="Enter Password",
                            required=True,
                            minlength="8",
                            maxlength="100",
                            value="asd",  ### DEBUG
                        ),
                        Br(),
                        Input(
                            id="show_pwd",
                            name="show_pwd",
                            type="checkbox",
                            data_bind="is_show",
                        ),
                        Label("Show Password", _for="show_pwd"),
                    ),
                    Button("Log In"),
                    Span(f" or "),
                    A("Sign Up", href=signup),
                ),
            ),
            html_footer(),
        ),
    )


@auth_rt.post("/login_process")
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

    sess["name"] = u["name"]
    return Redirect(profile)


@auth_rt.get("/logout")
def logout(sess):
    # DEBUG
    # global db
    # db.close(sess["name"])

    del sess["name"]
    return Redirect("/")


@auth_rt.get("/signup")
def signup():
    return (
        Title(f"Signup: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(),
            Main(
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
                        ),
                        Label("Show Password", _for="show_pwd"),
                    ),
                    Button("Sign Up"),
                ),
            ),
            html_footer(),
        ),
    )


@auth_rt.post("/signup_process")
def signup_process(name: str, pwd: str, sess):
    if not name or not pwd:
        return Redirect(login)

    global db
    rows = list(db.app.query("SELECT 1 FROM user WHERE name=?", (name,)))

    if rows:  # there's already someone with that name
        return Redirect(signup)

    db.app.execute(
        "INSERT OR REPLACE INTO user (name, pwd) VALUES (?, ?)",
        (name, pwd_context.hash(pwd)),
    )

    sess["name"] = name
    return Redirect(profile)


@auth_rt.get("/profile")
def profile(sess):
    return (
        Title(f"Profile: Ay Gogh"),
        Body(
            A(Strong("Jump to content"), href="#main-heading", cls="skip-link"),
            html_header(sess),
            Main(
                H1("Profile", id="main-heading"),
                Section(
                    H2("Test"),
                    A("Browse", href="/test", _class="button"),
                ),
                Section(
                    H2("Read"),
                ),
            ),
            html_footer(sess),
        ),
    )
