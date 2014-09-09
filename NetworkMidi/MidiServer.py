""" IOStream based TCP server, along with connection handler methods.
    Huge credit goes to

        http://w.gdu.me/wiki/Python/Python_socket.html

    for inspiring this code.
"""
__author__ = 'John Fu, 2014.'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetworkMidi.EC2 import EC2Server
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop


class MidiTCPServer(TCPServer):
    """ Override handle_stream to initialize a connection. """
    def handle_stream(self, stream, address):
        print("New connection from:", address, stream)
        MidiConnectionHandler(stream, address)
        print(len(MidiConnectionHandler.clients), " clients connected")


class MidiConnectionHandler(object):
    """ Class for handling connections to the server. """
    clients = set()

    def __init__(self, stream, address):
        MidiConnectionHandler.clients.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self._read()
        print("A new user has entered the chat room: ", address)

    def _read(self):
        self._stream.read_until(b'\n', callback=self._broadcast)
 
    def _broadcast(self, data):
        print("User played:", data[:-1], self._address)
        for conn in MidiConnectionHandler.clients:
            conn.send_message(data)
        self._read()
 
    def send_message(self, data):
        self._stream.write(data)
 
    def on_close(self):
        print("A user has left .", self._address)
        MidiConnectionHandler.clients.remove(self)

 
if __name__ == '__main__':
    print("Server start ...")
    server = MidiTCPServer()
    server.listen(EC2Server.PORT, EC2Server.HOST)
    IOLoop.instance().start()