""" Transmits MIDI to channel 1 (whichever channel the keyboard is on)"""
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi
import time

midi_out = rtmidi.MidiOut()
midi_out.open_port(1)

flag = 1
while flag == 1:
    midi_out.send_message([0x90, 40, 60]) # Note on
    flag = 0