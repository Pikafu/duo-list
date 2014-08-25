# Echo client program
import socket
from MidiHandler.KeyboardMidi import LocalMidi

# Copy public DNS here
#AMAZON_DNS = 'ec2-54-200-119-164.us-west-2.compute.amazonaws.com'
#HOST = socket.gethostbyname(AMAZON_DNS)
HOST = "localhost"
PORT = 3000              # The same port as used by the server

# TCP Packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if __name__ == "__main__":
    l_midi = LocalMidi()    # local_midi
    l_midi.setup_local_midi()

    while True:
        tx_rtmidi, delta_time = l_midi.MIDI_IN.get_message()
        if tx_rtmidi:
            if l_midi.get_msg_type(tx_rtmidi[0]) is not l_midi.SYSEX_MSG:   # Don't send sysex messages, only concerned with note/sustain info
                s.sendall(bytearray(tx_rtmidi))                             # Send thru socket, bytearray conversion required
            else:
                s.sendall(bytearray(3))                                     # Send some empty packets for funs