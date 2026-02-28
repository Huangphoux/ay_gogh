from starhtml import *
import nats
import asyncio


from read import read_rt


hdrs = ()

# Embedded NATS

app, rt = star_app(hdrs=hdrs)
read_rt.to_app(app)


async def main():
    server = await nats.server.run(port=0, jetstream=True)
    nc = await nats.connect(servers=server.client_url)

    serve()

    await server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
