""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from MidiHandler.KeyboardMidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
import tornado.ioloop
import tornado.iostream
import socket
from time import sleep

def prepare_midi():
    while True:
        msg, delta_time = localmidi.MIDI_IN_CONN.get_message()
        if msg is not None and msg[0] is not localmidi.SYSEX_MSG:
            print(msg)
            stream.write(bytes(msg))
            #stream.read_bytes(num_bytes=16, partial=True, callback=print_from)

def print_from(data):
    print("received: ", data)

#def on_headers(data):
#    print("Received ", data)

#    def on_body(data):
#        print(data)
#        stream.close()
#        tornado.ioloop.IOLoop.instance().stop()

localmidi = LocalMidi()
localmidi.setup_local_midi()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream = tornado.iostream.IOStream(s)
stream.connect((EC2Server.HOST, EC2Server.PORT), prepare_midi)
tornado.ioloop.IOLoop.instance().start()
