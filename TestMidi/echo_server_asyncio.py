__author__ = 'John'
import asyncio
from TestMidi.EC2 import EC2Server

class EchoServer(asyncio.Protocol):
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
coro = loop.create_server(EchoServer, e.HOST, e.PORT)
server = loop.run_until_complete(coro)
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()