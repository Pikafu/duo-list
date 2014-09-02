__author__ = 'John'
import asyncio
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from NetworkMidi.EC2 import EC2Server


class EchoClient(asyncio.Protocol):

    def connection_made(self, transport):
        self.message = "Hey you, I'm sending you a message."
        transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))

    def data_received(self, data):
        print('transport received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server close the connection')
        asyncio.get_event_loop().stop()

e = EC2Server()
loop = asyncio.get_event_loop()
coro = loop.create_connection(EchoClient, e.HOST, e.PORT)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()