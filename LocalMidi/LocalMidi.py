""" Methods for local MIDI transmission and reception. """
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi


class LocalMidi:
    def __init__(self):
        self.ON_OFF = 'Note ON/OFF'
        self.C_CHG = 'Control Change'
        self.P_CHG = 'Program Change'
        self.EMU = 'E-MU'                           # Starting characters of name of midi to emu interface
        self.ON_OFF_RANGE = range(0x80, 0xA0)    # All possible MIDI note on/off channels
        self.C_CHG_RANGE = range(0xB0, 0xC0)       # Same for control change channels
        self.midi_out = rtmidi.MidiOut()
        self.midi_in = rtmidi.MidiIn()

    # Returns type of msg assuming a msg is received
    def get_msg_type(self, msg):
        if len(msg) == 3:
            if msg[0] in self.ON_OFF_RANGE:
                return self.ON_OFF
            elif msg[0] in self.C_CHG_RANGE:
                return self.C_CHG
        else:
            return self.P_CHG

    # Scans ports for E-MU MIDI to USB interface and then establishes
    # bi-directional communication between the digital keyboard and computer
    def setup_local_midi(self):
        for port_in in self.midi_in.ports:
            if port_in.startswith(self.EMU.encode()):
                try:
                    self.midi_in.open_port(port_in)
                except ValueError:
                    print('Could not open port ' + port_in.decode())
                else:
                    print('Connected to ' + port_in.decode())
        for port_out in self.midi_out.ports:
            if port_out.startswith(self.EMU.encode()):
                try:
                    self.midi_out.open_port(port_out)
                except ValueError:
                    print('Could not open port ' + port_out.decode())
                else:
                    print('Connected to ' + port_out.decode())