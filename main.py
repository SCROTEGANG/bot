import shelve
import asyncio

from bot import SCROTUS
import config


def main():
    db = shelve.DbfilenameShelf("scrotus.db")
    b = SCROTUS(db)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(b.start(config.TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(b.close())
    finally:
        db.close()
        loop.close()


if __name__ == "__main__":
    main()
