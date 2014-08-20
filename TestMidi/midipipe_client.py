# Echo client program
import socket
from LocalMidi import LocalMidi

# Copy public DNS here
AMAZON_DNS = "ec2-54-201-111-7.us-west-2.compute.amazonaws.com"
HOST = socket.gethostbyname(AMAZON_DNS)
#HOST = "localhost"
PORT = 3000              # The same port as used by the server

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if __name__ == "__main__":
    localmidi = LocalMidi.LocalMidi()
    localmidi.setup_local_midi()

    while True:
        msg, delta_time = localmidi.midi_in.get_message()
        if msg:
            msg_in_bytes = bytearray(msg)
            s.sendall(msg_in_bytes)