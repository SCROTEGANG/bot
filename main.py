import os
import asyncio
import logging

from bot import SCROTUS


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def main():
    b = SCROTUS()

    token = os.getenv("SCROTUS_TOKEN")
    if token is None:
        log.fatal("$SCROTUS_TOKEN was not specified")
        return

    try:
        await b.start(token)
    except KeyboardInterrupt:
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
