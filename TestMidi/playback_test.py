""" Verifies local MIDI receive/transmit """
__author__ = 'John Fu, 2014.'

from LocalMidi.LocalMidi import KeyboardMidi

if __name__ == "__main__":
    localmidi = KeyboardMidi()
    localmidi.setup_local_midi()

    while True:
        msg, delta_time = localmidi.MIDI_IN.get_message()
        if msg:
            print(msg)
            msg_type, msg_max_length = localmidi.get_msg_info(msg[0])

            if msg_type == localmidi.ON_OFF:
                localmidi.MIDI_OUT.send_message([msg[0], msg[1] + 3, msg[2]])
            else:
                localmidi.MIDI_OUT.send_message(msg)