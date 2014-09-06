""" Implements client functions. """
__author__ = 'John Fu, 2014.'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from NetworkMidi.EC2 import EC2Server
import tornado.ioloop
import tornado.iostream
import socket

def send_request():
    print("Writing")
    stream.write("HELLO\n".encode())
    stream.read_until(b"\n", on_headers)

def on_headers(data):
    print("Received ", data)

"""def on_body(data):
    print(data)
    stream.close()
    tornado.ioloop.IOLoop.instance().stop()
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream = tornado.iostream.IOStream(s)
stream.connect((EC2Server.HOST, EC2Server.PORT), send_request)
tornado.ioloop.IOLoop.instance().start()