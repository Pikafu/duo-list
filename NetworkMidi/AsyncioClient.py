""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import asyncio


class MidiClient(asyncio.Protocol):

    def connection_made(self, transport):
        self.message = "Hey you, I'm sending you a message."
        transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))

    def data_received(self, data):
        print('transport received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server close the connection')
        asyncio.get_event_loop().stop()