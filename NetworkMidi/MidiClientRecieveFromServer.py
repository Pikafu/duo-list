""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import socket
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError


class TCPClientRx(object):
    def __init__(self, host, port, localmidi):
        self.host = host
        self.port = port
        self.localmidi = localmidi

    @coroutine
    def connect(self):
        conn = ReceiveFromServer(self.host, self.port, self.localmidi)
        print("Connected TCPClient RX: ", self.host, self.port)
        yield conn.start()


class ReceiveFromServer(object):
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
        yield self._send_to_keyboard()

    @coroutine
    def _send_to_keyboard(self):
        try:
            while True:
                msg = yield self.stream.read_until(b'\n')
                m = memoryview(msg[:-1]).tolist()
                print("received ", msg[:-1], " and converted to ", m)
                self.localmidi.MIDI_OUT_CONN.send_message(m)
        except StreamClosedError:
            pass

    def on_disconnect(self):
        print("Disconnected client: ", self._host, self._port)
        self.localmidi.cleanup_ports()