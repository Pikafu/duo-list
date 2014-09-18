""" Instantiates server/client variables. """
__author__ = 'John Fu, 2014.'

import socket


class EC2Server:
    AMAZON_DNS = 'ec2-54-68-7-241.us-west-2.compute.amazonaws.com'
    #HOST = 'localhost'
    HOST = socket.gethostbyname(AMAZON_DNS)
    PORT = 3001              # Arbitrary high port
