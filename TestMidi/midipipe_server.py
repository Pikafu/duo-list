# Echo server program
import socket
from MidiHandler.KeyboardMidi import LocalMidi

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 3000               # Arbitrary non-privileged port

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

if __name__ == "__main__":
    r_midi = LocalMidi()    # remote midi
    while True:
        #status = conn.recv(1)
        #type, max_len = r_msg.get_msg_info(status)    # Handles varying payload sizes
        #payload = conn.recv(max_len-1)
        #msg_in_bytes = status + payload    # concat those bytearrays
        msg_in_bytes = conn.recv(r_midi.NORMAL_MAX_PAYLOAD)    # Assume no sysex messages made it
        print(memoryview(msg_in_bytes).tolist())