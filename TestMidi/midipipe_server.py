# Echo server program
import socket
from LocalMidi import LocalMidi

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 3000               # Arbitrary non-privileged port
localmidi = LocalMidi.LocalMidi()

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

if __name__ == "__main__":
    while True:
        # Handles messages of varying payload sizes
        startbyte = conn.recv(1)
        msg_type, msg_max_length = localmidi.get_msg_info(startbyte)
        msg_in_bytes = conn.recv(msg_max_length)

        if msg_in_bytes:
            msg = memoryview(msg_in_bytes).tolist()
            print(msg)
        #if not data: break