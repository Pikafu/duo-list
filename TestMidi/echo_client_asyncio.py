__author__ = 'John'
import asyncio

class EchoClient(asyncio.Protocol):
    message = "hey you, yea you, I'm talking to you"

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))

    def data_received(self, data):
        print('transport received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server close the connection')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
coro = loop.create_connection(EchoClient, 'localhost', 3001)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()