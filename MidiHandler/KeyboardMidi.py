""" Methods for local MIDI transmission and reception. """
__author__ = 'John Fu, 2014.'

import rtmidi_python as rtmidi


class LocalMidi:
    def __init__(self):
        self.ON_OFF = 'Note ON/OFF'
        self.ON = 'Note ON'
        self.OFF = 'Note OFF'
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
        self.MIDI_OUT_CONN = rtmidi.MidiOut()
        self.MIDI_IN_CONN = rtmidi.MidiIn()

    def get_msg_type(self, msg):
        """ Reads the status int (from an rtmidi message).
            If not a system exclusive message, return the type. Otherwise, return True. """
        status = msg[0]
        velocity = msg[2]
        if status in self.ON_OFF_RANGE:
            if status in self.ON_OFF_RANGE[0:15] or velocity == 0:
                return self.OFF
            else:
                return self.ON
        elif status in self.C_CHG_RANGE:
            return self.C_CHG
        elif status in self.P_CHG_RANGE:
            return self.P_CHG
        elif status in self.P_BEND_RANGE:
            return self.P_BEND_CHG
        elif status is self.SYSEX_START:
            return self.SYSEX_MSG

    def setup_local_midi(self):
        """ Scans ports for E-MU MIDI to USB interface and then establishes
            bi-directional communication between the digital keyboard and computer. """
        for port_in in self.MIDI_IN_CONN.ports:
            if port_in.startswith(self.EMU.encode()):
                try:
                    self.MIDI_IN_CONN.open_port(port_in)
                except ValueError:
                    print('Could not open port ' + port_in.decode())
                else:
                    print('Connected to ' + port_in.decode())
        for port_out in self.MIDI_OUT_CONN.ports:
            if port_out.startswith(self.EMU.encode()):
                try:
                    self.MIDI_OUT_CONN.open_port(port_out)
                except ValueError:
                    print('Could not open port ' + port_out.decode())
                else:
                    print('Connected to ' + port_out.decode())

    def cleanup_ports(self):
        """ Closes all the input and output ports. """
        self.MIDI_IN_CONN.close_port()
        self.MIDI_IN_CONN = None
        self.MIDI_OUT_CONN.close_port()
        self.MIDI_OUT_CONN = None