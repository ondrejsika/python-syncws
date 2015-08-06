from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from crochet import wait_for, setup, run_in_reactor
from twisted.internet import reactor


class WSP(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.callbacks['onOpen'](self)

    def onClose(self, wasClean, code, reason):
        self.factory.callbacks['onClose'](self, wasClean, code, reason)

    def onConnect(self, request):
        self.factory.callbacks['onConnect'](self, request)

    def onMessage(self, payload, isBinary):
        self.factory.callbacks['onConnect'](self, payload, isBinary)


class WSF(WebSocketServerFactory):
    protocol = WSP
    callbacks = {
        'onOpen': lambda *args: args,
        'onClose': lambda *args: args,
        'onConnect': lambda *args: args,
        'onMessage': lambda *args: args,
    }
    _sessions = {}

    def buildProtocol(self, addr):
        protocol = WSP()
        protocol.factory = self
        self._sessions[addr] = protocol
        return protocol

    def sendToAll(self, payload, isBinary=False):
        for session in self._sessions.itervalues():
            session.sendMessage(payload, isBinary)


class SyncWS(object):
    _target = None
    _port = None

    def __init__(self, port):
        setup()
        self._target = WSF()
        self._port = port
        self.setup()

    @run_in_reactor
    def setup(self):
        # from twisted.python import log
        # import time
        # log.startLogging(open('/tmp/syncws-%s.log' % int(time.time()), 'w'))
        reactor.listenTCP(self._port, self._target)

    @wait_for(timeout=10)
    def sendToAll(self, payload, isBinary=False):
        return self._target.sendToAll(payload, isBinary)
