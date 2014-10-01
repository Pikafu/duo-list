""" IOStream based TCP client using Threads and Queues to exchange MIDI packets
    to and from the connected hardware. Thank you

        niltoid -       http://niltoid.com/blog/raspberry-pi-arduino-tornado/

    for inspiring the Queue based approach for passing information between threads. """
__author__ = 'John Fu, 2014.'

import os
import sys
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MidiHandler.keyboardmidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
from queue import Queue
from threading import Thread

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError
from time import sleep, clock


class MidiTCPClient():
    def __init__(self, host, port):
        self.conn = MidiConnectionHandler(host, port)

    @coroutine
    def connect(self):
        yield self.conn.start()

class MidiConnectionHandler(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.keyboard_listener = Queue()
        self.server_listener = Queue()
        self._localmidi = LocalMidi()
        self._localmidi.setup_local_midi()
        self.stream = IOStream(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.stream.set_close_callback(self.on_disconnect)
        self.timer = 0

    @coroutine
    def start(self):
        yield self.stream.connect((self._host, self._port))   # This returns a future so need @coroutine decorator
        print("Connected to: ", self._host, self._port)
        Thread(target=self.listen_keyboard, args=()).start()
        Thread(target=self.dispatch_server, args=()).start()
        Thread(target=self.listen_server, args=()).start()
        #Thread(target=self.dispatch_keyboard, args=()).start()
        Thread(target=self.dispatch_keyboard_chords, args=()).start()

    def listen_keyboard(self):
        """ Thread for listening to output from the keyboard and putting it into the keyboard listener queue. """
        # Import globals to local scope for faster looping
        ON = self._localmidi.ON
        OFF = self._localmidi.OFF
        SUS = self._localmidi.SUS
        while True:
            rtmidi_msg, delta_time = self._localmidi.MIDI_IN_CONN.get_message()
            if rtmidi_msg is not None:
                msg_type = self._localmidi.get_msg_type(rtmidi_msg)
                if msg_type == ON or msg_type == OFF or msg_type == SUS:
                    self.keyboard_listener.put(bytes(rtmidi_msg)+b'\n')     # Encode for server's read_until method

    @coroutine
    def dispatch_server(self):
        """ Thread for retrieving notes from the keyboard listener queue and sending them to the server. """
        while True:
            if not self.keyboard_listener.empty():
                rtmidi_msg_bytes = self.keyboard_listener.get()
                yield self.stream.write(rtmidi_msg_bytes)

    @coroutine
    def listen_server(self):
        """ Thread for listening to output from the server and putting it into the server listener queue. """
        while True:
            msg_bytes = yield self.stream.read_until(delimiter=b'\n')
            self.server_listener.put(msg_bytes[:-1])    # Strip \n

    def dispatch_keyboard(self):
        """ Thread for retrieving input from the server listener queue and sending it to the keyboard. """
        while True:
            if not self.server_listener.empty():
                msg_bytes = self.server_listener.get()
                print(msg_bytes)
                self._localmidi.MIDI_OUT_CONN.send_message(msg_bytes)

    def dispatch_keyboard_chords(self):
        """ Thread for retrieving input from the server listener queue and sending it to the keyboard. """
        while True:
            if not self.server_listener.empty():
                msg_list = self.get_chord(self.server_listener, max_notes=10)
                # print(msg_list)
                # Play chords
                for msg in msg_list:
                    self._localmidi.MIDI_OUT_CONN.send_message(msg)

    def get_chord(self, queue, max_notes):
        """ Get up to max_notes midi packets from the queue. """
        chord = []
        r = range(0, max_notes)
        for notes_retrieved in r:
            try:
                if notes_retrieved == max_notes:
                    break
                chord.append(queue.get_nowait())
            except Exception as e:
                pass
        return chord

    def on_disconnect(self):
        print("Disconnected client: ", self._host, self._port)
        self._localmidi.cleanup_ports()


if __name__ == "__main__":
    m = MidiTCPClient(EC2Server.HOST, EC2Server.PORT)
    m.connect()
    IOLoop.instance().start()