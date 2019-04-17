#!/usr/bin/env python3

# buttons.py, functions to work with the list of buttons and their mapping to
# remote power control devices
# Copyright (C) 2019  John Snowdon
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

from lib import config
from lib.newlog import newlog

# Set up a logger for this file
logger = newlog(__file__)

def getAllButtons():
	""" Return all buttons / devices """
	
	buttons = []
	for p in getPages():
		buttons += getButtons(p, "L")
		buttons += getButtons(p, "R")
		
	return buttons

def getPages():
	""" Return screen list """
	
	screens = list(config.SCREENS.keys())
	screens.sort()
	return screens
	
def getButtons(page = 1, align = "L"):
	""" Return the buttons for a screen """
	
	buttons = []
	
	if page in getPages():
		try:
			button_numbers = config.SCREENS[page]['BUTTON'][align].keys()
			for button_number in button_numbers:
				button = config.SCREENS[page]['BUTTON'][align][button_number]
				# Add in the alignment and button number
				button['align'] = align
				button['number'] = button_number
				buttons.append(button)
		except Exception as e:
			logger.warn(e)
			buttons = []
		
	return buttons

def getButtonsForTag(tag = None, exclude = None):
	""" Return all buttons/devices with the matching tag, except those with a title matching exclude """
	
	buttons = []
	for page in getPages():
		for align in ["L", "R"]:
			for button_number in config.SCREENS[page]['BUTTON'][align].keys():
				if tag in config.SCREENS[page]['BUTTON'][align][button_number]['tags']:
					if config.SCREENS[page]['BUTTON'][align][button_number]['text'] != exclude:
						buttons.append(config.SCREENS[page]['BUTTON'][align][button_number])
	return buttons

def getButtonPower(button):
	""" Return the power state of a device represented by a button """
	
	pass

def setButtonPower(energenie = None, button = None, state = "ON"):
	""" Send a power state message to a device represented by a button """
	
	
	logger.info("Sending power %s signal" % state)
	if state == "ON":
		action_type = 'poweron'
		
	if state == 'OFF':
		action_type = 'poweroff'
		
	if action_type in button.keys():
		
		if len(button[action_type]) > 0:
			# Unroll the poweron/off action list
			for action in button[action_type]:
				
				# Is it a composite/macro action?
				if 'tags' in action.keys():
					logger.debug("Macro action")
					
					# Find all of the devices/buttons (except the current one) with this tag
					buttons = []
					for t in action['tags']:
						buttons += getButtonsForTag(tag = t, exclude = button['text'])
						
					for b in buttons:
						logger.debug("Calling %s.%s with %s [%s]" % (b['remote'], b['socket'], action['action'], b['text']))
						
						# Create device and send signal
						if energenie:
							for d in energenie['buttons']:
								if (d['remote'] == b['remote']) and (d['socket'] == b['socket']):
									if action['action'] == "ON":
										d.turn_on()
									if action['action'] == "OFF":
										d.turn_off()
				else:
					# Single fire action, just call with remote id and socket id
					logger.debug("Single fire action")
					logger.debug("Calling %s.%s with %s" % (action['remote'], action['socket'], action['action']))
					
					# Create device and send signal
					if energenie:
						for d in energenie['buttons']:
							if (d['remote'] == action['remote']) and (d['socket'] == action['socket']):
								if action['action'] == "ON":
									d.turn_on()
								if action['action'] == "OFF":
									d.turn_off()
		else:
			# No power entries defined, just send a power signal to the defined remote and socket
			logger.warn("No %s action entries defined - using default remote and socket" % action_type)
			sent = False
			for d in energenie['buttons']:
				if (d['remote'] == button['remote']) and (d['socket'] == button['socket']) and (d['text'] == button['text']):
					if state == "ON":
						d['device'].turn_on()
						sent = True
					if state == "OFF":
						d['device'].turn_off()
						sent = True
			if sent:
				logger.debug("Sent signal to %s.%s" % (str(hex(d['remote'])), d['socket']))
			else:
				logger.warn("Signal not sent to %s.%s" % (str(hex(d['remote'])), d['socket']))
	else:
		logger.warn("No %s action defined" % action_type)
	
def getPowerMonitor(energenie = None):
	""" Listen for any broadcast power signals """
	
	
	# Listen for broadcasts
	return 