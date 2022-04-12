import os
import asyncio
import logging

import asyncpg
from bot import SCROTUS


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def main():
    token = os.getenv("SCROTUS_TOKEN")
    if token is None:
        log.fatal("$SCROTUS_TOKEN was not specified")
        return

    dsn = os.getenv("SCROTUS_DSN")
    if dsn is None:
        log.fatal("$SCROTUS_DSN was not specified")
        return

    conn = await asyncpg.connect(dsn=dsn)
    b = SCROTUS(conn)

    try:
        await b.start(token)
    except KeyboardInterrupt:
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
