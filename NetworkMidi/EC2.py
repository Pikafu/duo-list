""" Instantiates server/client variables. """
__author__ = 'John Fu, 2014.'

import socket


class EC2Server:
    def __init__(self):
        # IP of the E2C server instance this code is running on
        #self.HOST = "localhost"
        self.AMAZON_DNS = 'ec2-54-68-7-241.us-west-2.compute.amazonaws.com'
        self.HOST = socket.gethostbyname(self.AMAZON_DNS)
        self.PORT = 3001              # Arbitrary high port