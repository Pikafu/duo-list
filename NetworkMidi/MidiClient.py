""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import os
import sys
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MidiHandler.KeyboardMidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError


class MidiTCPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @coroutine
    def connect(self):
        conn = MidiConnectionHandler(self.host, self.port)
        print("Connected to: ", self.host, self.port)
        yield conn.start()


class MidiConnectionHandler(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._localmidi = LocalMidi()
        self._localmidi.setup_local_midi()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = IOStream(s)
        self.stream.set_close_callback(self.on_disconnect)
        #IOLoop.instance().start()
        print("started")
        return
        #self.start()

    @coroutine
    def start(self):
        yield self.stream.connect((EC2Server.HOST, EC2Server.PORT))
        print("In start")
        yield self._send_and_receive()
        #yield self._poll_from_keyboard()
        #return

    # On read:
    # Send to keyboard
    # Poll for midi runs in the background and writes

    @coroutine
    def _send_and_receive(self):
        try:
            while True:
                print("polling to send: ")
                remote_rx = yield self.stream.read_until(b'\n')
                m = memoryview(remote_rx[:-1]).tolist()
                print("received ", remote_rx[:-1], " and converted to ", m)
                #self._localmidi.MIDI_OUT_CONN.send_message(m)
                local_rx, delta_time = self._localmidi.MIDI_IN_CONN.get_message()
                if local_rx is not None and local_rx[0] is not self._localmidi.SYSEX_MSG:
                    yield self.stream.write(bytes(local_rx) + '\n'.encode())  
                    print("sent midi packet ", bytes(local_rx) + '\n'.encode())
        except StreamClosedError:
            pass

    @coroutine
    def _send_to_keyboard(self):
        try:
            while True:
                print("polling to send: ")
                msg = yield self.stream.read_until(b'\n')
                m = memoryview(msg[:-1]).tolist()
                print("received ", msg[:-1], " and converted to ", m)
                #self._localmidi.MIDI_OUT_CONN.send_message(m)
        except StreamClosedError:
            pass

    @coroutine
    def _poll_from_keyboard(self):
        """ Polls the connected MIDI device for incoming data, then sends it. """
        while True:
            msg, delta_time = self._localmidi.MIDI_IN_CONN.get_message()
            if msg is not None and msg[0] is not self._localmidi.SYSEX_MSG:
                print("Got note")
                yield self.stream.write(bytes(msg) + '\n'.encode())
                print("sent midi packet")

    def on_disconnect(self):
        print("Disconnected client: ", self._host, self._port)
        self._localmidi.cleanup_ports()

#def on_headers(data):
#    print("Received ", data)

#    def on_body(data):
#        print(data)
#        stream.close()
#        tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    m = MidiTCPClient(EC2Server.HOST, EC2Server.PORT)
    m.connect()
    IOLoop.instance().start()