""" Verifies local MIDI receive/transmit """
__author__ = 'John Fu, 2014.'

import sys
import os

# from MidiHandler.KeyboardMidi import LocalMidi
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from MidiHandler.KeyboardMidi import LocalMidi

if __name__ == "__main__":
    localmidi = LocalMidi()
    localmidi.setup_local_midi()

    # # Testing pedal
    # pedamidiin, port_name = open_midiport(port)l = [[176, 64, 0],[176, 64, 127],[176, 64, 104],[176, 64, 127]]
    # note1_on = [144, 44, 49]
    # note1_off = [144, 44, 0]
    # note2_on = [144, 46, 52]
    # note2_off = [144, 46, 0]
    # pedal_off = [176, 64, 0]

    # # Press pedal then send short note and hold pedal for 2 seconds
    # for n in pedal:
    #     localmidi.MIDI_OUT_CONN.send_message(n)
    # time.sleep(0.1)
    # localmidi.MIDI_OUT_CONN.send_message(note1_on)
    # time.sleep(0.1)
    # localmidi.MIDI_OUT_CONN.send_message(note1_off)
    # time.sleep(2)
    # localmidi.MIDI_OUT_CONN.send_message(pedal_off)

    try:
        # timer = time.time()
        while True:
            message = localmidi.MIDI_IN_CONN.get_message()

            if message:
                msg, delta_time = message
                msg_type = localmidi.get_msg_type(msg)
                print("Received: ", msg, " of type ", msg_type)
                localmidi.MIDI_OUT_CONN.send_message([msg[0], msg[1]+3, msg[2]])

            #time.sleep(0.01)

    except KeyboardInterrupt as e:
        print(e)
    finally:
        print("Exit.")
        localmidi.MIDI_IN_CONN.close_port()
        localmidi.MIDI_OUT_CONN.close_port()
        localmidi.cleanup_ports()

    #     if msg:
    #         msg_type = localmidi.get_msg_type(msg)
    #         print(msg)
    #         if msg_type in [localmidi.ON, localmidi.OFF]:
    #             localmidi.MIDI_OUT_CONN.send_message([msg[0], msg[1]+3, msg[2]])
    #         if msg_type in [localmidi.SUS]:
    #             localmidi.MIDI_OUT_CONN.send_message(msg)