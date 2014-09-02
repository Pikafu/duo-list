""" Transmits MIDI from locally attached keyboard and receives MIDI from remote keyboard(s) """
__author__ = 'John Fu, 2014.'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from NetworkMidi.EC2 import EC2Server
from NetworkMidi.AsyncioClient import MidiClient


if __name__ == "__main__":
    ec2 = EC2Server()
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(MidiClient, ec2.HOST, ec2.PORT)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()