#!/usr/bin/env python3

# Pair an arbitrary number of Energenie green button sockets
# with a new sequence of house codes. These can be ANY number you
# wish.

import time
import energenie

APP_DELAY = 1

energenie.init()

# I have at least 16 power strips, so I set up
# at least 16 new house codes here for them to learn
ADDRESSES = [
0xA0001,
0xA0002,
0xA0003,
0xA0004,
0xA0005,
0xA0006,
0xA0007,
0xA0008,
0xA0009,
0xA000A,
0xA000B,
0xA000C,
0xA000D,
0xA000E,
0xA0010,
0xA0011
]

# For each unique house code
for a in ADDRESSES:
    print("")
    print("Stage 0. Training device for code [%s]" % hex(a))
    rerun = True
    while rerun:
        s = energenie.Devices.OOKSwitch((a, 1))
        print("Stage 1. Put power switch [%s] in learn mode then press enter..." % hex(a))
        print("- SEND ON")
        s.turn_on()
        time.sleep(1)
        print("- SEND ON")
        s.turn_on()
        time.sleep(1)
        print("- SEND ON")
        s.turn_on()
        # Check that the correct power strip has turned on here, 
        print("Stage 2. Check that the correct power strip has activated")
        print("")
        print("Relearn this socket? (y/n)...")
        c = input()
        if c == "n":
            rerun = False
            print("")

