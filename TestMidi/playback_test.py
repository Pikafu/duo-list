""" Verifies local MIDI receive/transmit """
__author__ = 'John Fu, 2014.'

from MidiHandler.KeyboardMidi import LocalMidi

if __name__ == "__main__":
    localmidi = LocalMidi()
    localmidi.setup_local_midi()

    while True:
        msg, delta_time = localmidi.MIDI_IN_CONN.get_message()
        if msg:
            print(msg)
            msg_type = localmidi.get_msg_type(msg[0])
            if msg_type == localmidi.ON_OFF:
                localmidi.MIDI_OUT_CONN.send_message([msg[0], msg[1] + 3, msg[2]])
            else:
                localmidi.MIDI_OUT_CONN.send_message(msg)