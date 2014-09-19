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
from time import sleep


class MidiTCPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @coroutine
    def connect(self):
        conn = MidiConnectionHandler(self.host, self.port)
        yield conn.start()

class MidiConnectionHandler(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.keyboard_listener = Queue()
        self.server_listener = Queue()
        self._localmidi = LocalMidi()
        self._localmidi.setup_local_midi()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = IOStream(s)
        self.stream.set_close_callback(self.on_disconnect)

    @coroutine
    def start(self):
        print("start called")
        yield self.stream.connect((self._host, self._port))   # This returns a future so need @coroutine decorator
        print("Connected to: ", self._host, self._port)

        Thread(target=self.listen_to_keyboard, args=()).start()
        Thread(target=self.dispatch_to_server, args=()).start()

        Thread(target=self.listen_to_server, args=()).start()
        Thread(target=self.dispatch_to_keyboard, args=()).start()

    def listen_to_keyboard(self):
        """ Thread for listening to output from the keyboard and putting it into the keyboard listener queue. """
        while True:
            rtmidi_msg, time = self._localmidi.MIDI_IN_CONN.get_message()
            if rtmidi_msg is not None and rtmidi_msg[0] is not self._localmidi.SYSEX_MSG:     # Do not store SYSEX messages
                self.keyboard_listener.put(rtmidi_msg)
                print(rtmidi_msg)

    @coroutine
    def dispatch_to_server(self):
        """ Thread for retrieving notes from the keyboard listener queue and sending them to the server. """
        while True:
            if not self.keyboard_listener.empty():
                rtmidi_msg = self.keyboard_listener.get()
                yield self.stream.write(bytes(rtmidi_msg) + b'\n')     # Encode and concat with \n

    @coroutine
    def listen_to_server(self):
        """ Thread for listening to output from the server and putting it into the server listener queue. """
        while True:
            msg_bytes = yield self.stream.read_until(delimiter=b'\n')
            self.server_listener.put(msg_bytes)

    def dispatch_to_keyboard(self):
        """ Thread for retrieving input from tje server listener queue and sending it to the keyboard. """
        while True:
            if not self.server_listener.empty():
                msg_bytes = self.server_listener.get()
                msg = memoryview(msg_bytes[:-1]).tolist()  # Assuming contents of queue still have \n, strip them
                self._localmidi.MIDI_OUT_CONN.send_message(msg)

    def on_disconnect(self):
        print("Disconnected client: ", self._host, self._port)
        self._localmidi.cleanup_ports()


if __name__ == "__main__":
    m = MidiTCPClient(EC2Server.HOST, EC2Server.PORT)
    m.connect()
    IOLoop.instance().start()