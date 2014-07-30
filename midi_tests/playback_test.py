""" Polls channel 0 for input MIDI """
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi

N_ON_OFF = 'Note ON/OFF'
C_CHG = 'Control Change'
P_CHG = 'Program Change'
emu = 'E-MU' # starting characters of name of midi to emu interface

# Note ON/OFF - msg[0] is 8nH or 9nH
# Program change - msg[0] > BnH
# 128 144 176

# Returns type of msg assuming a msg is received
def get_msg_type(msg):
    if len(msg) == 3:
        if 0x80 <= msg[0] <= 0x9F:
            return N_ON_OFF
        elif 0xB0 <= msg[0] <= 0xBF:
            return C_CHG
    else:
        return P_CHG

midi_in = rtmidi.MidiIn()
for in_port in midi_in.ports:
    print(in_port)
    if in_port.startswith(emu.encode()):
        try:
            midi_in.open_port(in_port)
        except ValueError as e:
            print('Could not open port ' + in_port)
        else:
            print('Connected to ' + in_port)

midi_out = rtmidi.MidiOut()
for out_port in midi_out.ports:
    print(out_port)
    if out_port.startswith(emu.encode()):
        try:
            midi_out.open_port(out_port)
        except ValueError as e:
            print('Could not open port ' + out_port)
        else:
            print('Connected to ' + out_port)

while True:
    msg, delta_time = midi_in.get_message()
    if msg:
        msg_type = get_msg_type(msg)
        if msg_type == N_ON_OFF:
            midi_out.send_message([msg[0], msg[1] + 3, msg[2]])
        else:
            midi_out.send_message(msg)