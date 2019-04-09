#!/usr/bin/env python3

# sdlrfcontroller.py, display a SDL interface of clicky buttons which turn on/off RF 
# power sockets
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

import sys
import time
import timeit
import ctypes

from lib import config
from lib.newlog import newlog
from lib.buttons import getPages, getButtonPower, setButtonPower


# SDL routines
from sdl2 import *
from lib.gfx import gfxInit, gfxClose, gfxSplashScreen
from lib.render import renderPage, renderStatus

# Set up a logger for this file
logger = newlog(__file__)

def sdlRFController():
	
	# Defaults for first page shown
	running = True
	# Default transition effect
	transition = None
	# Initial page
	page = 1
	
	logger.info("Starting...")
	
	# Open an SDL display
	window = gfxInit()
	if window is False:
		logger.error("Unable to continue - Exit")
		return 1
	
	# Clear the canvas and show it
	window.clear()
	window.update()
	
	# Fade in/out a loading screen
	gfxSplashScreen(window)
	window.update()
	time.sleep(1.5)
	window.clear()
	window.update()
	
	# Show page 1
	renderPage(window = window, page = page)
	window.update(transition = transition)
	
	# SDL event handler
	event = SDL_Event()
	
	# Default switch mode
	power_mode = "ON"
	screen = "page"
	button = False
	clicked = False
	redraw = True
	
	# Event handler
	while running:
		time.sleep(config.REFRESH_TIME)
		while SDL_PollEvent(ctypes.byref(event)) != 0:
			
			if event.type == SDL_QUIT:
				# Handle the quit signal tasks (control-c, close of terminal, window etc)
				logger.info("Quit signal detected")
				running = False
				break				
				
			elif (event.type == SDL_KEYDOWN) or (event.type == SDL_MOUSEBUTTONDOWN) or (event.type == SDL_FINGERDOWN):
				################################################
				#
				# Handle keyboard or mouse input
				#
				################################################
				
				if event.type == SDL_KEYDOWN:
					logger.debug("Keyboard input")
					button = False
					clicked = False
				if (event.type == SDL_MOUSEBUTTONDOWN):
					window.mouseRead(event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("Mouse input [box:%s]" % clicked)
				if (event.type == SDL_FINGERDOWN):
					window.mouseRead(event)
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("Touch input [box:%s]" % clicked)
					
				if clicked == "deviceClick":
					# Flash the button to indicate click
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					
					# Run the device RF power command
					logger.info("Calling radio functions for button [%s:%s:%s remote:%s socket:%s]" % (page, button['align'], button['number'], button['remote'], button['socket']))
					setButtonPower(button, state = power_mode)
					redraw = False
					break
				
				if (clicked == "btn_config"):
					if screen == "status":
						# Go back to main pages
						renderStatus(window, button_clicked = button, flash = True, power_mode = power_mode)
						renderPage(window, page = page, button_clicked = button, flash = False, power_mode = power_mode)
						screen = "page"
						redraw = False
						break
					else:
						# Draw status screen
						renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
						renderStatus(window, button_clicked = button, flash = False, power_mode = power_mode)
						screen = "status"
						redraw = True
				
				if (screen == "page") and (clicked == "btn_power"):
					# Flash the button to indicate click
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
				
					# Change power button mode
					if power_mode == "ON":
						power_mode = "OFF"
					else:
						power_mode = "ON"
						
					# Redraw screen
					redraw = True
					break
				
				if (event.key.keysym.sym == SDLK_q):
					# Exit from the running application
					running = False
					break
				
				if (screen == "page") and ((event.key.keysym.sym == SDLK_RIGHT) or (clicked == "btn_fwd")):
					# Forward a page
					button = window.boxPressedByName(name = "btn_fwd")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page < getPages()[-1]:
						page += 1
					else:
						page = 1
					redraw = True
					break
						
				if (screen == "page") and ((event.key.keysym.sym == SDLK_LEFT) or (clicked == "btn_back")):
					# Back a page
					button = window.boxPressedByName(name = "btn_back")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page > 1:
						page -= 1
					else:
						page = getPages()[-1]
					redraw = True
					break
						
			else:
				# Unsupported event type - just redraw the current screen
				pass
			
		if redraw:
			# Because of user input, redraw the chosen screen
			if screen == "page":
				renderPage(window, page = page, button_clicked = button, flash = False, power_mode = power_mode)
				redraw = False
			if screen == "status":
				renderStatus(window, button_clicked = button, flash = False, power_mode = power_mode)
			window.update(transition = transition)
		
	# Clean up the SDL libary
	gfxClose()
	return 0
	
if __name__ == '__main__':
	sys.exit(sdlRFController())