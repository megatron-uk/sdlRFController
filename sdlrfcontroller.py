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


# SDL routines
from sdl2 import *
from lib.gfx import *

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
	time.sleep(2)
	window.clear()
	window.update()
	
	# Show page 1
	gfxPage(window = window, page = page)
	window.update(transition = transition)
	
	# SDL event handler
	event = SDL_Event()
	
	# Event handler
	while running:
		redraw = False
		time.sleep(0.05)
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
					logger.info("Keyboard input")
					clicked = False
				if (event.type == SDL_MOUSEBUTTONDOWN):
					window.mouseRead()
					clicked = window.boxPressed()
					logger.info("Mouse input [box:%s]" % clicked)
				if (event.type == SDL_FINGERDOWN):
					window.mouseRead()
					clicked = window.boxPressed()
					logger.info("Touch input [box:%s]" % clicked)
				
				if (event.key.keysym.sym == SDLK_q):
					# Exit from the running application
					running = False
					break
				
				if (event.key.keysym.sym == SDLK_RIGHT) or (clicked == "btn_fwd"):
					# Forward a page
					page += 1
					redraw = True
						
				if (event.key.keysym.sym == SDLK_LEFT) or (clicked == "btn_back"):
					# Back a page
					if page > 1:
						page -= 1
					redraw = True
						
				if redraw:
					# Because of user input, redraw the chosen screen
					page = gfxPage(window = window, page = page)
					window.update(transition = transition)
					break
			else:
				# Unsupported event type - just redraw the current screen
				pass
		
	# Clean up the SDL libary
	gfxClose()
	return 0
	
if __name__ == '__main__':
	sys.exit(sdlRFController())