""" Methods for local MIDI transmission and reception. """
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi


class LocalMidi:
    def __init__(self):
        self.n_on_off = 'Note ON/OFF'
        self.c_chg = 'Control Change'
        self.p_chg = 'Program Change'
        self.emu = 'E-MU'                           # Starting characters of name of midi to emu interface
        self.n_on_off_arr = range(0x80, 0xA0)    # All possible MIDI note on/off channels
        self.c_chg_arr = range(0xB0, 0xC0)       # Same for control change channels
        self.midi_out = rtmidi.MidiOut()
        self.midi_in = rtmidi.MidiIn()

    # Returns type of msg assuming a msg is received
    def get_msg_type(self, msg):
        if len(msg) == 3:
            if msg[0] in self.n_on_off_arr:
                return self.n_on_off
            elif msg[0] in self.c_chg_arr:
                return self.c_chg
        else:
            return self.p_chg

    # Scans ports for E-MU MIDI to USB interface and then establishes
    # bi-directional communication between the digital keyboard and computer
    def setup_local_midi(self):
        for port_in in self.midi_in.ports:
            if port_in.startswith(self.emu.encode()):
                try:
                    self.midi_in.open_port(port_in)
                except ValueError:
                    print('Could not open port ' + port_in.decode())
                else:
                    print('Connected to ' + port_in.decode())
        for port_out in self.midi_out.ports:
            if port_out.startswith(self.emu.encode()):
                try:
                    self.midi_out.open_port(port_out)
                except ValueError:
                    print('Could not open port ' + port_out.decode())
                else:
                    print('Connected to ' + port_out.decode())