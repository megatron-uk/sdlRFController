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

import os
import sys
import time
import timeit
import ctypes

from lib import config
from lib.newlog import newlog
from lib.buttons import getPages, getButtonPower, setButtonPower
from lib.pitft_touchscreen import pitft_touchscreen

# SDL routines
from sdl2 import *
from lib.gfx import gfxInit, gfxClose, gfxSplashScreen
from lib.render import renderPage, renderStatus, renderConfirmWindow

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

	# Try to init touchscreen
	try:
		ts = pitft_touchscreen()
		logger.info("Touchscreen input enabled")
	except Exception as e:
		logger.warn("Touchscreen input not available")
		logger.debug(e)
		ts = False

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
	sdl_event = SDL_Event()
	
	# Default switch mode
	power_mode = "ON"
	screen = "page"
	old_screen = "page"
	button = False
	clicked = False
	redraw = True
	loop_count = 0
	
	# Start collecting touchscreen input
	if ts:
		ts.start()
	# Event handler
	while running:
		
		# Dump any cached surfaces or fonts
		if loop_count > config.CACHE_CLEAR_TIME:
			window.clearCache()	
			loop_count = 0
			
		time.sleep(config.REFRESH_TIME)
		
		# Reset events
		sdl_event = False
		ts_event = False
		
		if ts:
			# Read ann touchscreen events
			while not ts.queue_empty():
				for e in ts.get_event():
					ts_event = e
					logger.info("Touch event [%s]" % ts_event)
					# Map x and y coordinates
					if 'y' in ts_event.keys():
						if config.TOUCH['axis_reversed']:
							window.touch_y_raw = ts_event['x']
						else:
							window.touch_y_raw = ts_event['y']
					if 'x' in ts_event.keys():
						if config.TOUCH['axis_reversed']:
							window.touch_x_raw = ts_event['y']
						else:
							window.touch_x_raw = ts_event['x']
		else:
			# Read an SDL event, if there is one
			SDL_PollEvent(ctypes.byref(sdl_event))
			
		if ((sdl_event != 0)  and (sdl_event.type != 0)) or (ts_event != False) :
			if ts_event:
				logger.debug("Process Touch event [%s]" % ts_event)
			if sdl_event:
				logger.debug("Process SDL event [%s type %s]" % (sdl_event, sdl_event.type))
			loop_count += 1	
			if (sdl_event and (sdl_event.type)) == SDL_QUIT:
				# Handle the quit signal tasks (control-c, close of terminal, window etc)
				logger.info("Quit signal detected")
				running = False
				#break				
				
			if (sdl_event and (sdl_event.type in [SDL_KEYDOWN, SDL_MOUSEBUTTONDOWN, SDL_FINGERDOWN, SDL_FINGERMOTION])) or (ts_event):
				################################################
				#
				# Handle keyboard or mouse input
				#
				################################################
				
				if (sdl_event and (sdl_event.type == SDL_KEYDOWN)):
					logger.debug("SDL Keyboard input")
					button = False
					clicked = False
				if (sdl_event and (sdl_event.type == SDL_MOUSEBUTTONDOWN)):
					window.mouseRead(sdl_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("SDL Mouse input [box:%s]" % clicked)
				if (sdl_event and (sdl_event.type == SDL_FINGERDOWN)):
					window.mouseRead(sdl_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("SDL Touch input [box:%s]" % clicked)
					
				if (ts_event):
					window.touchRead(ts_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("Touchscreen input [box:%s]" % clicked)
				
				#break
				
				if clicked == "deviceClick":
					# Flash the button to indicate click
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					
					# Run the device RF power command
					logger.info("Calling radio functions for button [%s:%s:%s remote:%s socket:%s]" % (page, button['align'], button['number'], button['remote'], button['socket']))
					setButtonPower(button, state = power_mode)
					redraw = False
					#break
				
				if (clicked == "btn_restart"):
					old_screen = screen
					renderConfirmWindow(window = window, header = "Application Restart", text = "This will restart the application.\nAre you sure?")
					screen = "restart"
					redraw = False
					#break
				
				if (screen == "restart") and (clicked == "btn_confirm"):
					# Restart application
					logger.info("Restarting application")
					python = sys.executable
					os.execl(python, python, *sys.argv)
					
				if (screen == "restart") and (clicked == "btn_cancel"):
					# Cancel restart overlay
					screen = old_screen
					redraw = True
					#break
				
				if (sdl_event and (sdl_event.key.keysym.sym == SDLK_s)) or (clicked == "btn_config"):
					button = window.boxPressedByName(name = "btn_config")		
					if screen == "status":
						# Go back to main pages
						renderStatus(window, button_clicked = button, flash = True, power_mode = power_mode)
						renderPage(window, page = page, button_clicked = button, flash = False, power_mode = power_mode)
						screen = "page"
						redraw = False
						#break
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
					#break
				
				if sdl_event:
					if (sdl_event.key.keysym.sym == SDLK_q):
						# Exit from the running application
						running = False
						#break
				
				if (screen == "page") and ((sdl_event and (event.key.keysym.sym == SDLK_RIGHT)) or (clicked == "btn_fwd")):
					# Forward a page
					button = window.boxPressedByName(name = "btn_fwd")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page < getPages()[-1]:
						page += 1
					else:
						page = 1
					redraw = True
					#break
						
				if (screen == "page") and ((sdl_event and (event.key.keysym.sym == SDLK_LEFT)) or (clicked == "btn_back")):
					# Back a page
					button = window.boxPressedByName(name = "btn_back")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page > 1:
						page -= 1
					else:
						page = getPages()[-1]
					redraw = True
					#break
						
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

        # Stop touchscreen
	if ts:
		ts.stop()
	return 0
	
if __name__ == '__main__':
	sys.exit(sdlRFController())
