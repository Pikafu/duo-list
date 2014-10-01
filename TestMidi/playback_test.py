""" Verifies local MIDI receive/transmit """
__author__ = 'John Fu, 2014.'

from MidiHandler.keyboardmidi import LocalMidi
import time

if __name__ == "__main__":
    localmidi = LocalMidi()
    localmidi.setup_local_midi()

    # Testing pedal
    pedal = [[176, 64, 0],[176, 64, 127],[176, 64, 104],[176, 64, 127]]
    note1_on = [144, 44, 49]
    note1_off = [144, 44, 0]
    note2_on = [144, 46, 52]
    note2_off = [144, 46, 0]
    pedal_off = [176, 64, 0]

    # Press pedal then send short note and hold pedal for 2 seconds
    for n in pedal:
        localmidi.MIDI_OUT_CONN.send_message(n)
    time.sleep(0.1)
    localmidi.MIDI_OUT_CONN.send_message(note1_on)
    time.sleep(0.1)
    localmidi.MIDI_OUT_CONN.send_message(note1_off)
    time.sleep(2)
    localmidi.MIDI_OUT_CONN.send_message(pedal_off)

    # while True:
    #     msg, delta_time = localmidi.MIDI_IN_CONN.get_message()
    #     if msg:
    #         msg_type = localmidi.get_msg_type(msg)
    #         print(msg)
    #         if msg_type in [localmidi.ON, localmidi.OFF]:
    #             localmidi.MIDI_OUT_CONN.send_message([msg[0], msg[1]+3, msg[2]])
    #         if msg_type in [localmidi.SUS]:
    #             localmidi.MIDI_OUT_CONN.send_message(msg)
