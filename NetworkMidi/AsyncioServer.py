""" Implements server functions. """
__author__ = 'John Fu, 2014.'

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from NetworkMidi.EC2 import EC2Server

class MidiServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print('data received {}'.format(data.decode()))
        self.transport.write(data)
        #close the socket
        self.transport.close()

e = EC2Server()
loop = asyncio.get_event_loop()
coro = loop.create_server(MidiServer, e.HOST, e.PORT)
server = loop.run_until_complete(coro)
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()
