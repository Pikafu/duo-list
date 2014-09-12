__author__ = 'John'
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tornado.ioloop import IOLoop
from MidiHandler.KeyboardMidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
from NetworkMidi.MidiClientRecieveFromServer import TCPClientRx, ReceiveFromServer
from NetworkMidi.MidiClientTransmitToServer import TCPClientTx, TransmitToServer

if __name__ == "__main__":
    midi_conn = LocalMidi()
    midi_conn.setup_local_midi()
    tx = TCPClientTx(EC2Server.HOST, EC2Server.PORT, midi_conn)
    #rx = TCPClientRx(EC2Server.HOST, EC2Server.PORT, midi_conn)
    tx.connect()
    #rx.connect()
    IOLoop.instance().start()