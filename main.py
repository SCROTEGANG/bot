import asyncio
import logging

from bot import SCROTUS
import config


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def main():
    b = SCROTUS()

    try:
        await b.start(config.TOKEN)
    except KeyboardInterrupt:
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
