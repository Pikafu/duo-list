__author__ = 'John'
import asyncio

class EchoClient(asyncio.Protocol):

    def __init__(self):
        # IP of the server instance this code is running on
        #AMAZON_DNS = 'ec2-54-68-7-241.us-west-2.compute.amazonaws.com'
        selfHOST = socket.gethostbyname(AMAZON_DNS)
        #self.HOST = "localhost"
        self.PORT = 3001              # The same port as used by the server
        self.message = "hey you, yea you, I'm talking to you"

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))

    def data_received(self, data):
        print('transport received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server close the connection')
        asyncio.get_event_loop().stop()

c = EchoClient()
loop = asyncio.get_event_loop()
coro = loop.create_connection(c, c.HOST, c.PORT)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()