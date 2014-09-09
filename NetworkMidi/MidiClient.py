""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import os
import sys
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MidiHandler.KeyboardMidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
from tornado.iostream import IOStream
from tornado.ioloop import IOLoop


class MidiTCPClient(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._localmidi = LocalMidi()
        self.start()

    def start(self):
        self._localmidi.setup_local_midi()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = IOStream(s)
        self.stream.connect((EC2Server.HOST, EC2Server.PORT), self._poll_from_keyboard)
        IOLoop.instance().start()
        #self._read()
        self._poll_from_keyboard()

    # On read:
    # Send to keyboard
    # Poll for midi runs in the background and writes

    def _read(self):
        self.stream.read_until(b'\n', callback=self._send_to_keyboard)

    def _send_to_keyboard(self, data):
        """ Received data is in bytes so need to convert to rtmidi tuple format. """
        m = memoryview(data).tolist()
        self._localmidi.MIDI_OUT_CONN.send_message(m)
        #self._poll_from_keyboard()

    def _poll_from_keyboard(self):
        """ Polls the connected MIDI device for incoming data, then sends it. """
        while True:
            msg, delta_time = self._localmidi.MIDI_IN_CONN.get_message()
            if msg is not None and msg[0] is not self._localmidi.SYSEX_MSG:
                print("sending: ", msg)
                self._send(msg)

    def _send(self, data):
        """ Sends data to the stream. """
        self.stream.write(bytes(data) + '\n'.encode())

#def on_headers(data):
#    print("Received ", data)

#    def on_body(data):
#        print(data)
#        stream.close()
#        tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    m = MidiTCPClient(EC2Server.HOST, EC2Server.PORT)
    m.start()
    #IOLoop.instance().start()