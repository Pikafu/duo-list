__author__ = 'John'
import asyncio
import socket

class EchoServer(asyncio.Protocol):

    def __init__(self):
        # IP of the server instance this code is running on
        #self.HOST = "localhost"
        AMAZON_DNS = 'ec2-54-68-7-241.us-west-2.compute.amazonaws.com'
        self.HOST = socket.gethostbyname(AMAZON_DNS)
        self.PORT = 3001              # The same port as used by the server
        self.transport = ""

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print('data received {}'.format(data.decode()))
        self.transport.write(data)
        #close the socket
        self.transport.close()

e = EchoServer()
loop = asyncio.get_event_loop()
coro = loop.create_server(e, e.HOST, e.PORT)
server = loop.run_until_complete(coro)
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()