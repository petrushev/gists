from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.python import log
from twisted.application.service import Service, Application

from txpostgres.txpostgres import Connection

class Listener(object):

    def __init__(self, connection):
        self._conn = connection

    def start(self):
        log.msg('Listening...')
        self._conn.addNotifyObserver(self.received)
        self._conn.runOperation("listen some_channel")\
                  .addErrback(self.onPollError)

    def onPollError(self, failure):
        log.err('Poll error: ' + failure.getErrorMessage())

    def received(self, notification):
        #do something with notification.payload
        pass

class ListenService(Service):

    def __init__(self, params):
        self._dbParams = params

    def startService(self):
        conn = Connection()
        conn.connect(self._dbParams)\
            .addCallback(self.onConnect)\
            .addErrback(self.onConnectErr, conn)

    def onConnect(self, connection):
        self._listener = Listener(connection)

        deferLater(reactor, 0, self._listener.start)\
            .addErrback(self.onListenError, self._listener)

    def onConnectErr(self, failure, connection):
        log.err('Error connecting to %s: %s' % (repr(connection), failure.getErrorMessage()))

    def onListenError(self, failure, listener):
        log.err('Listener %s failed to start: %s' % (repr(listener), failure.getErrorMessage()))


dbParams = {}

application = Application("Postgresql channel listener")
ListenService(params = dbParams).setServiceParent(application)
