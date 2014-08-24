""" Methods for local MIDI transmission and reception. """
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi


class KeyboardMidi:
    def __init__(self):
        self.ON_OFF = 'Note ON/OFF'
        self.C_CHG = 'Control Change'
        self.P_CHG = 'Program Change'
        self.P_BEND_CHG = 'Pitch Bend Change'
        self.SYSEX_MSG = 'System Exclusive Message'
        self.EMU = 'E-MU'                           # Starting characters of MIDI to USB interface
        self.ON_OFF_RANGE = range(0x80, 0xA0)       # All possible MIDI note on/off channels
        self.C_CHG_RANGE = range(0xB0, 0xC0)        # Same for control change channels
        self.P_CHG_RANGE = range(0xC0, 0xD0)
        self.P_BEND_RANGE = range(0xE0, 0xF0)
        self.SYSEX_START = 0xF0
        self.NORMAL_MAX_PAYLOAD = 3                 # Max payload size for note ON/OFF, control change, mode, and program change
        self.SYSEX_MAX_PAYLOAD = 12                 # Max payload size for system exclusive messages
        self.MIDI_OUT = rtmidi.MidiOut()
        self.MIDI_IN = rtmidi.MidiIn()

    # Returns [length of message, payload length] based on the start byte received
    def get_msg_info(self, startbyte):
        if startbyte in self.ON_OFF_RANGE:
            return [self.ON_OFF, self.NORMAL_MAX_PAYLOAD]
        elif startbyte in self.C_CHG_RANGE:
            return [self.C_CHG, self.NORMAL_MAX_PAYLOAD]
        elif startbyte in self.P_CHG_RANGE:
            return [self.P_CHG, self.NORMAL_MAX_PAYLOAD]
        elif startbyte in self.P_BEND_RANGE:
            return [self.P_BEND_CHG, self.NORMAL_MAX_PAYLOAD]
        elif startbyte is self.SYSEX_START:
            return [self.SYSEX_MSG, self.SYSEX_MAX_PAYLOAD]
        else:
            return None

    # Scans ports for E-MU MIDI to USB interface and then establishes
    # bi-directional communication between the digital keyboard and computer
    def setup_local_midi(self):
        for port_in in self.MIDI_IN.ports:
            if port_in.startswith(self.EMU.encode()):
                try:
                    self.MIDI_IN.open_port(port_in)
                except ValueError:
                    print('Could not open port ' + port_in.decode())
                else:
                    print('Connected to ' + port_in.decode())
        for port_out in self.MIDI_OUT.ports:
            if port_out.startswith(self.EMU.encode()):
                try:
                    self.MIDI_OUT.open_port(port_out)
                except ValueError:
                    print('Could not open port ' + port_out.decode())
                else:
                    print('Connected to ' + port_out.decode())