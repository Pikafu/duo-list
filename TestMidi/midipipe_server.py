# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 3000               # Arbitrary non-privileged port

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

if __name__ == "__main__":
    while True:
        data = conn.recv(1024)
        if data:
            msg = memoryview(data).tolist()
            print(msg)
        #if not data: break