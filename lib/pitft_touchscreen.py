# -*- coding: utf-8 -*-
#  piTFT touchscreen handling using evdev

#
# This code was taken from: https://github.com/PrzemoF/pitft_touchscreen
#
# pitft_touchscreen.py, piTFT touchscreen handling with evdev
# Copyright (C) 2018  PrzemoF
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import evdev
except ImportError:
    print("Evdev package is not installed.  Run 'pip3 install evdev' or 'pip install evdev' (Python 2.7) to install.")
    raise(ImportError("Evdev package not found."))
import threading
try:
    # python 3.5+
    import queue
except ImportError:
    # python 2.7
    import Queue as queue


# Class for handling events from piTFT
class pitft_touchscreen(threading.Thread):
    def __init__(self, device_path="/dev/input/touchscreen", grab=False):
        super(pitft_touchscreen, self).__init__()
        self.device_path = device_path
        self.grab = grab
        self.events = queue.Queue()
        self.shutdown = threading.Event()

    def run(self):
        thread_process = threading.Thread(target=self.process_device)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()
        self.shutdown.wait()

    # thread function
    def process_device(self):
        device = None
        # if the path to device is not found, InputDevice raises an OSError
        # exception.  This will handle it and close thread.
        try:
            device = evdev.InputDevice(self.device_path)
            if self.grab:
                device.grab()
        except Exception as ex:
            message = "Unable to load device {0} due to a {1} exception with" \
                      " message: {2}.".format(self.device_path,
                                              type(ex).__name__, str(ex))
            raise Exception(message)
        finally:
            if device is None:
                self.shutdown.set()
        # Loop for getting evdev events
        event = {'time': None, 'id': None, 'x': None, 'y': None, 'touch': None}
        dropping = False
        while not self.shutdown.is_set():
            for input_event in device.read_loop():
                if input_event.type == evdev.ecodes.EV_ABS:
                    if input_event.code == evdev.ecodes.ABS_X:
                        event['x'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_Y:
                        event['y'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_MT_TRACKING_ID:
                        event['id'] = input_event.value
                        if input_event.value == -1:
                            event['x'] = None
                            event['y'] = None
                            event['touch'] = None
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_X:
                        pass
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                        pass
                elif input_event.type == evdev.ecodes.EV_KEY:
                    event['touch'] = input_event.value
                elif input_event.type == evdev.ecodes.SYN_REPORT:
                    if dropping:
                        event['x'] = None
                        event['y'] = None
                        event['touch'] = None
                        dropping = False
                    else:
                        event['time'] = input_event.timestamp()
                        self.events.put(event)
                        e = event
                        event = {'x': e['x'], 'y': e['y']}
                        try:
                            event['id'] = e['id']
                        except KeyError:
                            event['id'] = None
                        try:
                            event['touch'] = e['touch']
                        except KeyError:
                            event['touch'] = None
                elif input_event.type == evdev.ecodes.SYN_DROPPED:
                    dropping = True
        if self.grab:
            device.ungrab()

    def get_event(self):
        if not self.events.empty():
            event = self.events.get()
            yield event
        else:
            yield None

    def queue_empty(self):
        return self.events.empty()

    def stop(self):
        self.shutdown.set()

    def __del__(self):
        self.shutdown.set()
