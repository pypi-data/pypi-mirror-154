#!/usr/bin/env python3
"""
Reads & Prints KISS frames from a Serial console.

Mac OS X Tests
--------------

Soundflower, VLC & Dire Wolf as an audio-loopback-to-socket-bridge:

    1. Select "Soundflower (2ch)" as Audio Output.
    2. Play 'test_frames.wav' via VLC: `open -a vlc test_frames.wav`
    3. Startup direwolf: `direwolf -p "Soundflower (2ch)"`
    4. Run this script.


Dire Wolf as a raw-audio-input-to-socket-bridge:

    1. Startup direwolf: `direwolf -p - < test_frames.wav`
    2. Run this script.


Test output should be as follows:

    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  1 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  2 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  3 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  4 of 4

"""
import os

import ax253
import kiss


KISS_SERIAL = os.environ.get("KISS_SERIAL", "/dev/cu.Repleo-PL2303-00303114")
KISS_SPEED = os.environ.get("KISS_SPEED", "9600")


def print_frame(frame):
    print((ax253.Frame.from_bytes(frame)))


def main():
    ki = kiss.SerialKISS(port=KISS_SERIAL, speed=KISS_SPEED, strip_df_start=True)
    ki.start()
    ki.read(callback=print_frame, min_frames=1)


if __name__ == "__main__":
    main()
