""" Methods for local MIDI transmission and reception. """
__author__ = 'John Fu, 2014.'

import rtmidi


class LocalMidi:
    def __init__(self):
        self.ON_OFF = 'Note ON/OFF'
        self.ON = 'Note ON'
        self.OFF = 'Note OFF'
        self.C_CHG = 'Control Change'
        self.SUS = 'Sustain'
        self.P_CHG = 'Program Change'
        self.P_BEND_CHG = 'Pitch Bend Change'
        self.SYSEX_MSG = 'System Exclusive Message'
        self.EMU = 'E-MU'                           # Starting characters of MIDI to USB interface

        self.ON_OFF_RANGE = range(0x80, 0xA0)       # All possible MIDI note on/off channels
        self.C_CHG_RANGE = range(0xB0, 0xC0)        # Same for control change channels
        self.P_CHG_RANGE = range(0xC0, 0xD0)
        self.P_BEND_RANGE = range(0xE0, 0xF0)

        self.NOTE_OFF_VELOCITY = 0
        self.SUSTAIN_MSB = 0x40
        self.SYSEX_START = 0xF0

        self.MIDI_OUT_CONN = rtmidi.MidiOut()
        self.MIDI_IN_CONN = rtmidi.MidiIn()

    def get_msg_type(self, msg):
        """ Reads the status int (from an rtmidi message).
            If not a system exclusive message, return the type. Otherwise, return True. """
        status = msg[0]
        if status in self.ON_OFF_RANGE:
            if not msg[2] == self.NOTE_OFF_VELOCITY:
                return self.ON
            else:
                return self.OFF
        elif status in self.C_CHG_RANGE:
            if msg[1] == self.SUSTAIN_MSB:
                return self.SUS
            return self.C_CHG
        elif status in self.P_CHG_RANGE:
            return self.P_CHG
        elif status in self.P_BEND_RANGE:
            return self.P_BEND_CHG
        elif status is self.SYSEX_START:
            return self.SYSEX_MSG

    # TO DO: PASS IN MIDI IN AND MIDI OUT AS LOCAL VARIABLES
    def setup_local_midi(self):
        """ Scans ports for E-MU MIDI to USB interface and then establishes
            bi-directional communication between the digital keyboard and computer. """
        avail_in = self.MIDI_IN_CONN.get_ports()
        avail_out = self.MIDI_OUT_CONN.get_ports()

        for port_in in avail_in:
            if port_in.startswith(self.EMU):
                try:
                    self.MIDI_IN_CONN.open_port(avail_in.index(port_in))
                except ValueError:
                    print('Could not open port ' + port_in)
                else:
                    print('Connected to ' + port_in)
        for port_out in avail_out:
            if port_out.startswith(self.EMU):
                try:
                    self.MIDI_OUT_CONN.open_port(avail_out.index(port_out))
                except ValueError:
                    print('Could not open port ' + port_out)
                else:
                    print('Connected to ' + port_out)

    def cleanup_ports(self, midiin, midiout):
        """ Closes all the input and output ports. """
        midiin.close_port()
        del midiin
        midiout.close_port()
        del midiout
