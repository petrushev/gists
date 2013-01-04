import sys

def deal(dealer, data, spawn_worker, poll_timeout=2000):
    """Deals 'data' to workers through 'dealer' as they become available
       Spawns new worker with 'spawn_worker' if not available during 'poll_timeout' """
    while True:
        polled = dealer.poll(timeout=2000) # wait for available worker
        if polled == 0: # not available
            spawn_worker()

        else: # available worker
            _ = dealer.recv()
            dealer.send(data)
            return

def catch(worker, handler):
    """Catches data from 'worker' and processes it by 'handler'."""
    worker.send('') # request job
    data = worker.recv() # job received
    try:
        handler(data)
    except Exception, exc: # fail tolerance
        sys.stderr.write("%s: %s\n" % (sys.exc_info()[0].__name__, exc))
