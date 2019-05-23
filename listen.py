#!/usr/bin/env python3

import time
import energenie

APP_DELAY = 1

energenie.init()
mon1 = energenie.registry.get('mon1')
mon2 = energenie.registry.get('mon2')
mon3 = energenie.registry.get('mon3')
mon4 = energenie.registry.get('mon4')
mons = [mon1, mon2, mon3, mon4]

print("======")

while True:
    energenie.loop()
    time.sleep(1)
    print("")
    print("==========================")
    for mon in mons:
        r = mon.get_readings()
        print("%s v" % r.voltage)
        #print("%s A" % r.current)
        print("%s w (real)" % r.real_power)
        #print("%s w (apparent)" % r.apparent_power)
        print("%s w (reactive)" % r.reactive_power)
        print("%s Hz" % r.frequency)
        print("-")
