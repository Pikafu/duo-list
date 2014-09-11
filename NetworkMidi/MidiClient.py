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
        s = yield self.stream.connect((EC2Server.HOST, EC2Server.PORT))
        print("In start")
        #yield [self._poll_from_keyboard(s), self.read()]
        yield self.read()
        #self._poll_from_keyboard()
        #return

    # On read:
    # Send to keyboard
    # Poll for midi runs in the background and writes

    @coroutine
    def read(self):
        try:
            while True:
                msg = yield self.stream.read_until(b'\n')
                print("received from server: ", msg[:-1])
                m = memoryview(msg[:-1]).tolist()
                self._localmidi.MIDI_OUT_CONN.send_message(m)
        except StreamClosedError:
            pass

    def _send_to_keyboard(self, data):
        """ Received data is in bytes so need to convert to rtmidi tuple format. """
        m = memoryview(data).tolist()
        self._localmidi.MIDI_OUT_CONN.send_message(m)
        #self._poll_from_keyboard()

    @coroutine
    def _poll_from_keyboard(self, stream):
        """ Polls the connected MIDI device for incoming data, then sends it. """
        print("polling for midi: ")
        while True:
            msg, delta_time = self._localmidi.MIDI_IN_CONN.get_message()
            if msg is not None and msg[0] is not self._localmidi.SYSEX_MSG:
                yield stream.write(bytes(msg) + '\n'.encode())
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