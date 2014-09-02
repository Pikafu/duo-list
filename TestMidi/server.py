""" Transmits MIDI from linked keyboards to all other keyboards in the pool. """
__author__ = 'John Fu, 2014.'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from NetworkMidi.EC2 import EC2Server
from NetworkMidi.AsyncioServer import MidiServer


if __name__ == "__main__":
    ec2 = EC2Server()
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MidiServer, ec2.HOST, ec2.PORT)
    server = loop.run_until_complete(coro)
    print('serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        server.close()
        loop.close()