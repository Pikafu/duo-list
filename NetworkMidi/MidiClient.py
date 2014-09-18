""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import os
import sys
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MidiHandler.keyboardmidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
from multiprocessing import Queue
from threading import Thread

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError


class MidiTCPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.keyboard_listener = Queue()

    def connect(self):
        conn = MidiConnectionHandler(self.host, self.port)
        print("Connected to: ", self.host, self.port)
        conn.start()


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

    def start(self):
        self.stream.connect((EC2Server.HOST, EC2Server.PORT))
        print("In start")
        Thread(target=self._send_to_keyboard, args=()).start()
        Thread(target=self._poll_from_keyboard, args=()).start()

    @coroutine
    def _send_to_keyboard(self):
        try:
            while True:
                msg_bytes = yield self.stream.read_until(b'\n')
                msg = memoryview(msg_bytes[:-1]).tolist()
                print("received ", msg_bytes, " and converted to ", msg)
                msg_type = self._localmidi.get_msg_type(msg[0])
                if msg_type == self._localmidi.ON_OFF:
                    self._localmidi.MIDI_OUT_CONN.send_message([msg[0], msg[1] + 3, msg[2]])
                else:
                    self._localmidi.MIDI_OUT_CONN.send_message(msg)

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


if __name__ == "__main__":
    m = MidiTCPClient(EC2Server.HOST, EC2Server.PORT)
    m.connect()
    IOLoop.instance().start()