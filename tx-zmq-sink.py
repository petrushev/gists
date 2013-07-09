from twisted.application.service import Service, Application
from txzmq import ZmqFactory, ZmqEndpoint, ZmqPullConnection

def processor(data):
    """Called when the sink receives data"""
    print data[0]

class PullListener(Service):

    def __init__(self, port, bindAddress = '*'):
        self._bindAddress = 'tcp://%s:%d' % (bindAddress, port)

    def startService(self):
        zf = ZmqFactory()
        endpoint = ZmqEndpoint('bind', self._bindAddress)

        puller = ZmqPullConnection(zf, endpoint)
        puller.onPull = processor

application = Application('Data sink')
PullListener(5050).setServiceParent(application)
