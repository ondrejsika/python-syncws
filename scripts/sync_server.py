from syncws import SyncWS
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('port', help='Websocket server port', type=int)
args = parser.parse_args()

ws = SyncWS(args.port)

while True:
    ws.sendToAll(raw_input())
