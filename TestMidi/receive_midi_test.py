""" Polls channel 0 for input MIDI """
__author__ = 'John Fu, Pedro Rittner. 2014.'

import rtmidi_python as rtmidi

midi_in = rtmidi.MidiIn()
midi_in.open_port(0)

while True:
    message, delta_time = midi_in.get_message()
