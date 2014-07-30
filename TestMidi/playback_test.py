""" Verifies local MIDI receive/transmit """
__author__ = 'John Fu, Pedro Rittner. 2014.'

from LocalMidi import LocalMidi

if __name__ == "__main__":
    localmidi = LocalMidi.LocalMidi()
    localmidi.setup_local_midi()

    while True:
        msg, delta_time = localmidi.midi_in.get_message()
        if msg:
            print(msg)
            msg_type = localmidi.get_msg_type(msg)

            if msg_type == localmidi.n_on_off:
                localmidi.midi_out.send_message([msg[0], msg[1] + 3, msg[2]])
            else:
                localmidi.midi_out.send_message(msg)