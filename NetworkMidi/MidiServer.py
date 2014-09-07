import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from MidiHandler.KeyboardMidi import LocalMidi
from NetworkMidi.EC2 import EC2Server
import errno
import functools
import socket
from tornado import ioloop, iostream
 
 
class MidiConnection(object):
    def __init__(self, connection):
        self.stream = iostream.IOStream(connection)
        self._read()
 
    def _read(self):
        self.stream.read_bytes(num_bytes=16, partial=True, callback=self._eol_callback)
 
    def _eol_callback(self, data):
        self.handle_data(data)


class MidiClient(MidiConnection):
    """Put your app logic here"""
    def handle_data(self, data):
        print(data)
        self.stream.write(data)
        self._read()


def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind((EC2Server.HOST, EC2Server.PORT))
    sock.listen(1)
    return sock


def connection_ready(sock, fd, events):
    while True:
        try:
            connection, address = sock.accept()
        except OSError as e:
            if e.errno not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        else:
            connection.setblocking(0)
            MidiClient(connection)
 
 
if __name__ == '__main__':
    sock = setup_socket()
    io_loop = ioloop.IOLoop.instance()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        print("exited cleanly")