from time import sleep

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def iter_notifications(engine, channels, poll_timeout=1.0):
    """Iterate signals from postgresql database at `engine`,
    sent on `channels`."""
    conn = engine.connect().connection # low level psycopg connection
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    for channel in channels:
        curs.execute("LISTEN %s;" % channel)

    while True:
        sleep(poll_timeout)
        conn.poll() # poll db for notifications
        while conn.notifies:
            yield conn.notifies.pop()
