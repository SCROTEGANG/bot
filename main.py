import asyncio

from bot import SCROTUS
import config


def main():
    b = SCROTUS()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(b.start(config.TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(b.close())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
