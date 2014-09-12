""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import socket
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError


class TCPClientTx():
    def __init__(self, host, port, localmidi):
        self.host = host
        self.port = port
        self.localmidi = localmidi

    @coroutine
    def connect(self):
        conn = TransmitToServer(self.host, self.port, self.localmidi)
        print("Connected TCPClient TX: ", self.host, self.port)
        yield conn.start()


class TransmitToServer(object):
    def __init__(self, host, port, localmidi):
        self._host = host
        self._port = port
        self.localmidi = localmidi
        self.stream = IOStream(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.stream.set_close_callback(self.on_disconnect)
        return

    @coroutine
    def start(self):
        yield self.stream.connect((self._host, self._port))
        self._poll_from_keyboard()

    @coroutine
    def receive_note_callback(self, message, time_stamp):
        if message is not None and message[0] is not self.localmidi.SYSEX_MSG:
            yield self.stream.write(bytes(message) + '\n'.encode())

    def _poll_from_keyboard(self):
        """ Polls the connected MIDI device for incoming data, then sends it. """
        while True:
            self.localmidi.MIDI_IN_CONN.callback = self.receive_note_callback

    def on_disconnect(self):
        print("Disconnected client: ", self._host, self._port)
        self.localmidi.cleanup_ports()