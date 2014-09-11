""" IOStream based TCP server, along with connection handler methods.
    Uses co-routines as opposed to callbacks for simplicity of code.
    Huge thank you and credit goes to

        XStar - http://w.gdu.me/wiki/Python/Python_socket.html
        picomancer - https://github.com/picomancer/echoserver/blob/d590b375304ced9bc0609b85270491f58eb6d788/echoserver.py

    for inspiring this code.
"""
__author__ = 'John Fu, 2014.'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetworkMidi.EC2 import EC2Server
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from tornado.iostream import StreamClosedError
from time import sleep


class MidiTCPServer(TCPServer):
    """ TCP server sets up an IOStream. Override handle_stream
        and pass these onto the connection handler. """
    @coroutine
    def handle_stream(self, stream, address):
        print("New connection from:", address, stream)
        conn = MidiConnectionHandler(stream, address)
        yield conn.on_connect()
        print(len(MidiConnectionHandler.clients), " clients connected")


class MidiConnectionHandler(object):
    """ Class for handling connections to the server. """
    clients = set()

    def __init__(self, stream, address):
        MidiConnectionHandler.clients.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_disconnect)
        #self._read()

    @coroutine
    def on_connect(self):
        print("A new user has joined from: ", self._address)
        yield self.broadcast()

    @coroutine
    def broadcast(self):
        try:
            while True:
                #m = yield self._stream.read_until(b'\n')
                #print("Received from client: ", m)
                #yield self._stream.write(m[:-1])
                test = [144, 46, 40]
                rx = bytes(test) + '\n'.encode()
                yield self._stream.write(rx)
                sleep(0.5)
                print('sending hello')
        except StreamClosedError:
            pass

    def on_disconnect(self):
        print("A user has left .", self._address)
        MidiConnectionHandler.clients.remove(self)

 
if __name__ == '__main__':
    print("Server start ...")
    server = MidiTCPServer()
    server.listen(EC2Server.PORT, EC2Server.HOST)
    IOLoop.instance().start()