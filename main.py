import wordle
from index import hero_page, profile_page
from load_env import is_debug
from starhtml import *
import os, shutil
from starlette_cramjam.compression import Compression
from starlette_cramjam.middleware import CompressionMiddleware
from shared import db, is_signed_in, template

import settings
import read
import test
import auth
import popup
import index


def set_name(req, sess):
    auth = req.scope["auth"] = sess.get("auth", None)
    if not auth:
        return Redirect("/")


auth_bware = Beforeware(
    set_name,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        "/",
        *(
            f"/auth/{path}"
            for path in ("login", "login_process", "signup", "signup_process")
        ),
    ],
)


app, rt = star_app(  # SessionMiddleware arguments are also in star_app
    debug=False,
    title="Ay Gogh!",
    htmlkw={"lang": "en"},
    before=(auth_bware,),
    exception_handlers={num: lambda req, exc: Redirect("/") for num in range(400, 600)}
    if not is_debug
    else {},
    middleware=(
        Middleware(
            CompressionMiddleware,
            compression=[Compression.br, Compression.zstd, Compression.gzip],
        ),
    ),
    static_path="static",
    # default_hdrs=False,
    hdrs=(  # keep / in href, if not, /auth/custom.css
        Link(rel="icon", href="https://fav.farm/📖"),  # favicon
        Link(rel="stylesheet", href="https://cdn.simplecss.org/simple.min.css"),
        
        Link(rel="stylesheet", href="/global.css"),
    ),
    sess_https_only=not is_debug,  # set Secure flag on cookies
    same_site="strict",
    # .sesskey can be read/write by anyone
    # chmod 600 .sesskey to only be able to read/write by owner
    datastar="cdn",
    inline_icons=True,
)

auth.rt.to_app(app)
test.rt.to_app(app)
read.rt.to_app(app)
popup.rt.to_app(app)
settings.rt.to_app(app)
wordle.rt.to_app(app)

@rt
def index(req, sess):
    auth = sess.get("auth", None)

    main = hero_page() if not is_signed_in(req, sess) else profile_page(auth)

    return template("Home", main, auth)


if __name__ == "__main__":
    print(
        "You are currently in DEBUG mode.\n\
The `db` folder will be DELETED after stopping the server.\n\
You have been warned."
    ) if is_debug else None

    serve(port=1984)
    # remember to add `server_header=False` to uvicorn.run
    # log_level="error" too

    # Clean-up after exiting

    os.remove("./.sesskey")
    shutil.rmtree("__pycache__")

    db.close_all()
    shutil.rmtree("db") if is_debug else None
