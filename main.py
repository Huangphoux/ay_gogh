from fasthtml.common import *
from monsterui.all import *


hdrs = Theme.blue.headers()
app, rt = fast_app(hdrs=hdrs)


@app.get("/")
def home():
    return Title("Page Demo"), Div(
        H1("Hello, World"), P("Some text"), P("Some more text")
    )


serve()
