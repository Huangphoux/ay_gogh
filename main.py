from fasthtml.common import *
from monsterui.all import *

from read import read_rt

hdrs = (
    Script()
)

# Embedded NATS
server = await nats.server.run(port=0, jetstream=True, store_dir=tmpdir)
nc = await nats.connect(servers=server.client_url)

app, rt = fast_app(hdrs=hdrs)
read_rt.to_app(app)

serve()
