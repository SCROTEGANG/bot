import shelve
import asyncio

from bot import SCROTUS


def main():
    db = shelve.open("scrotus.db")
    b = SCROTUS(db)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(b.start())
    except KeyboardInterrupt:
        loop.run_until_complete(b.close())
    finally:
        db.close()
        loop.close()
