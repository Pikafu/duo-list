# Echo client program
import socket

# Copy public DNS here
HOST = socket.gethostbyname('ec2-54-191-68-77.us-west-2.compute.amazonaws.com') #Translate a host name to IPv4 address format.
#HOST = 'localhost'
PORT = 3000              # The same port as used by the server
message = bytes('Hello, World', 'utf-8')

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(message)
data = s.recv(1024)
s.close()
print('Received', repr(data))