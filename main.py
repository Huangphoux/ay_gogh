from starhtml import *
import nats

from read import read_rt


hdrs = Script()

# Embedded NATS

app, rt = star_app(hdrs=hdrs)
read_rt.to_app(app)

async def main():
    server = await nats.server.run(port=0, jetstream=True)
    nc = await nats.connect(servers=server.client_url)

    await server.shutdown()


if __name__ == "__main__":
    serve()
