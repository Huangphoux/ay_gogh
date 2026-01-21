from fasthtml.common import *
from monsterui.all import *

from read import read_rt

hdrs = (
    Style("""
        .dark .sun-icon { display: inline; }
        .dark .moon-icon { display: none; }
        html:not(.dark) .sun-icon { display: none; }
        html:not(.dark) .moon-icon { display: inline; }
    """),
    Script()
)


app, rt = fast_app(hdrs=hdrs)

read_rt.to_app(app)


serve()
