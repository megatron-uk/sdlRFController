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