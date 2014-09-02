""" Implements server functions. """
__author__ = 'John Fu, 2014.'

import asyncio


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