""" Implements server functions. """
__author__ = 'John Fu, 2014.'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from NetworkMidi.EC2 import EC2Server
from tornado.tcpserver import TCPServer
from tornado import ioloop
from tornado import iostream
import socket


class MidiStream():
    def __init__(self, stream, address, server):
        #Initialize base params and call stream reader for next line
        self.stream = stream
        if self.stream.socket.family not in (socket.AF_INET, socket.AF_INET6):
            # Unix (or other) socket; fake the remote address
            address = ('0.0.0.0', 0)
        self.address = address
        self.server = server

    def read_from(self):
        print("in read_from")
        self.stream.read_bytes(128, callback=self.send_back, partial=True)

    def send_back(self, data):
        print("Writing back", data)
        self.stream.write(data)

class MidiServer(TCPServer):
    def handle_stream(self, stream, address):
        s = MidiStream(stream, address, server=self)
        s.read_from()

io_loop = ioloop.IOLoop.instance()
server = MidiServer()
server.listen(EC2Server.PORT, address="")
io_loop.start()