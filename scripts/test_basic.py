from syncws import SyncWS


ws = SyncWS(8888)
ws._target.callbacks['onOpen'] = lambda protocol: protocol.factory.sendToAll('Hello')


while True:
    ws.sendToAll(raw_input())


