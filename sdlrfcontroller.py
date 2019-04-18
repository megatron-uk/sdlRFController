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

# Locals
from lib import config
from lib.newlog import newlog
from lib.buttons import getAllButtons, getPages, getButtonPower, setButtonPower
from lib.pitft_touchscreen import pitft_touchscreen

# SDL routines
from sdl2 import *
from lib.gfx import gfxInit, gfxClose, gfxSplashScreen
from lib.render import renderPage, renderStatus, renderConfirmWindow, renderPowerMon, renderFlash

# Set up a logger for this file
logger = newlog(__file__)

# Energenie
elib = False
try:
	import energenie as elib
except Exception as e:
	logger.fatal("")
	logger.fatal("========================= WARNING! =============================")
	logger.fatal("You must have the pyenergenie library installed and configured")
	logger.fatal("to use this application fully.")
	logger.fatal("")
	logger.fatal("Make sure you edit 'pyenergenie/src/energenie/drv/spis.c' with")
	logger.fatal("your GPIO settings and then rebuild the driver with 'build_rpi'.")
	logger.fatal("================================================================")
	logger.fatal("")
elib = False

def sdlRFController():
	
	# SDL only listens for these types of input, all others are ignored
	sdl_detected_events = [SDL_KEYDOWN, SDL_MOUSEBUTTONDOWN, SDL_FINGERDOWN, SDL_FINGERMOTION, SDL_QUIT]
	
	# Defaults for first page shown
	running = True
	transition = None
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
	
	# Try to init touchscreen
	try:
		ts = pitft_touchscreen()
		if ts.is_enabled():
			logger.info("Touchscreen input enabled")
			ts.start()
		else:
			logger.warn("Touchscreen input not available")
			ts = False
	except Exception as e:
		logger.warn("Touchscreen input not available")
		logger.debug(e)
		ts = False
	
	# Start up the energenie radio interface library
	energenie_buttons = []
	energenie_monitors = []
	if elib:
		elib.init()
		# Load all energenie sockets
		for b in getAllButtons():
			b['device'] = elib.Devices.ENER002((b['remote'], b['socket']))
			energenie_buttons.append(b)
			logger.debug("Adding device %s.%s" % (str(hex(b['remote'])), b['socket']))
			
		# Load all energenie power monitor devices
		for k in config.POWER_MONITORS:
			d = elib.Devices.MIHO004(device_id = config.POWER_MONITORS[k]['deviceid'])
			energenie_monitors.append(d)
			logger.debug("Adding monitor %s" % (str(hex(config.POWER_MONITORS[k]['deviceid']))))
			
		logger.info("Added %s Energenie power socket devices" % len(energenie_buttons))
		logger.info("Added %s Energenie power monitor devices" % len(energenie_monitors))
	else:
		logger.warn("Energenie radio functions not available")
		
	energenie = {
		'lib' : elib,
		'buttons' : energenie_buttons,
		'monitors' : energenie_monitors,
	}		
	
	# Show page 1
	renderPage(window = window, page = page)
	window.update(transition = transition)
	
	# SDL event handler
	sdl_event = SDL_Event()
	for t in sdl_detected_events:
		logger.debug("SDL event type [%s]" % t)
	
	# TS / Evdev
	ts_event = False
	
	# Default switch mode
	power_mode = "ON"
	screen = "page"
	old_screen = "page"
	button = False
	clicked = False
	redraw = True
	loop_count = 0
	old_button = {'name' : None}
	old_time = time.time()
	last_ts = time.time()
		
	# Open up the radio device
	radio = None
	
	# Power data from any connected power socket monitor stations
	power_data = {}
		
	# Event handler
	while running:
		
		# Sleep a minimum amount of time each loop - we don't want to 
		# peg the cpu at 100% just looping...
		time.sleep(config.REFRESH_TIME)
		
		# Dump any cached surfaces or fonts
		if loop_count > config.CACHE_CLEAR_TIME:
			window.clearCache()	
			loop_count = 0
		
		# Read any broadcast power events and update data
		#if energenie['lib']:
		#	energenie['lib'].loop()
			#for d in energenie['monitors']:
			#	try:
			#		pwr = d.get_power()
			#		logger.debug(pwr)
			#	except:
			#		pass
		
		# Reset any touchscreen event
		ts_event = False
		
		# Read any available touchscreen events
		if ts:
			while not ts.queue_empty():
				for e in ts.get_event():
					ts_event = e
					logger.debug("Touch event [%s]" % ts_event)
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
		
		#############################################################
		#
		# This section only fires if an input event is detected
		#
		#############################################################
		
		# Read an SDL event, if there is one, or proceed to process a touchscreen event
		while (SDL_PollEvent(ctypes.byref(sdl_event))) or (ts_event != False):
			loop_count += 1
			
			if (sdl_event and (sdl_event.type)) == SDL_QUIT:
				################################################
				#
				# Handle the quit signal tasks (control-c, close of terminal, window etc)
				#
				################################################
				logger.info("Quit signal detected")
				running = False
				break				
				
			if (sdl_event and (sdl_event.type in sdl_detected_events)) or (ts_event):
				################################################
				#
				# Handle keyboard or mouse input
				#
				################################################
				
				# SDL Keyboard
				if (sdl_event and (sdl_event.type == SDL_KEYDOWN)):
					logger.debug("SDL Keyboard input")
					button = False
					clicked = False
					
				# SDL Mouse click
				if (sdl_event and (sdl_event.type == SDL_MOUSEBUTTONDOWN)):
					window.mouseRead(sdl_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("SDL Mouse input [box:%s]" % clicked)
					
				# SDL touch 
				if (sdl_event and (sdl_event.type == SDL_FINGERDOWN)):
					window.mouseRead(sdl_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("SDL Touch input [box:%s]" % clicked)
					
				# Linux evdev touchscreen
				if (ts_event):
					ts_interval = (ts_event['time'] - last_ts)
					if ts_interval < config.BUTTON_BOUNCE_TIME:
						logger.debug("Ignoring touchscreen input [%.2fs]" % ts_interval)
						ts_event = False
						break
					
					window.touchRead(ts_event)
					button = window.boxPressed()
					if button:
						clicked = button['name']
					else:
						clicked = False
					logger.debug("Touchscreen input [box:%s]" % clicked)
					
					# Debounce check - only allow multiple clicks to the
					# same button after a minimum time delay, to reduce 
					# button bouncing.
					if (button) and ('name' in button.keys()):
						if (old_button) and ('name' in old_button.keys()):
							if button['name'] == old_button['name']:
								double_click_time = time.time() - old_time
								if double_click_time < config.BUTTON_BOUNCE_TIME:
									# Break from loop and do no further processing of this button click
									logger.debug("Ignoring touchscreen input - possible button bounce [%.2fs < %ss]" % (double_click_time, config.BUTTON_BOUNCE_TIME))
									ts_event = False
									break
								else:
									logger.debug("Accepting touchscreen input - long double click [%.2fs]" % double_click_time)
							
					old_button = button
					old_time = time.time()
					last_ts = ts_event['time']
					
				#############################################################
				#
				# All the actions we do based on input are defined below
				#
				#############################################################
					
				# We clicked on a device button, so send a power signal to that device (and any child devices defined in its' poweron or poweroff fields)
				if clicked == "deviceClick":
					# Flash the button to indicate click
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					
					# Run the device RF power command
					logger.info("Calling radio functions for button [%s:%s:%s remote:%s socket:%s]" % (page, button['align'], button['number'], str(hex(button['remote'])), button['socket']))
					setButtonPower(energenie = energenie, button = button, state = power_mode)
					redraw = False
				
				# Show the 'do you want to restart' overlay message
				if (clicked == "btn_restart"):
					old_screen = screen
					renderConfirmWindow(window = window, header = "Application Restart", text = "This will restart the application.\nAre you sure?")
					screen = "restart"
					redraw = False
				
				# Restart application
				if (screen == "restart") and (clicked == "btn_confirm"):
					logger.info("Restarting application")
					python = sys.executable
					os.execl(python, python, *sys.argv)
					
				# Cancel restart overlay
				if (clicked == "btn_cancel"):
					screen = old_screen
					redraw = True
				
				if (clicked == "btn_power"):
					# Flash the button to indicate click
					renderFlash(window, page = page, button_clicked = button, power_mode = power_mode, screen = screen)
					
					# Change power button mode
					if power_mode == "ON":
						power_mode = "OFF"
					else:
						power_mode = "ON"
						
					# Redraw screen
					redraw = True
				
				# If we clicked the status/config button/key, toggle between status/config screen on/off.
				if (sdl_event and (sdl_event.key.keysym.sym == SDLK_s)) or (clicked == "btn_config"):
					button = window.boxPressedByName(name = "btn_config")		
					if (screen != "status"):
						# Draw status screen
						renderFlash(window, page = page, button_clicked = button, power_mode = power_mode, screen = screen)
						renderStatus(window, button_clicked = button, flash = False, power_mode = power_mode)
						screen = "status"
						redraw = True
					else:
						# Go back to main pages
						renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
						screen = "page"
						redraw = True
				
				# If we clicked the power monitor button/key, toggle between power monitor screen on/off.
				if (sdl_event and (sdl_event.key.keysym.sym == SDLK_p)) or (clicked == "btn_meter"):
					button = window.boxPressedByName(name = "btn_meter")	
					if (screen != "monitor"):
						# Flash the button to indicate click and change to the power monitor screen
						renderFlash(window, page = page, button_clicked = button, power_mode = power_mode, screen = screen)
						renderPowerMon(window, page = page, button_clicked = button, flash = False, power_mode = power_mode, power_data = power_data)
						#renderStatus(window, button_clicked = button, flash = False, power_mode = power_mode)
						screen = "monitor"
						redraw = True
					else:
						# Flash the button to indicate click and change back to the button page
						renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
						screen = "page"
						redraw = True
				
				# If we pressed the keyboard Q/q key, exit from the running application
				if (sdl_event and (sdl_event.key.keysym.sym == SDLK_q)):
					running = False
				
				# If we pressed the right cursor key, or clicked on the right button, scroll one page right
				if (screen == "page") and ((sdl_event and (sdl_event.key.keysym.sym == SDLK_RIGHT)) or (clicked == "btn_fwd")):
					button = window.boxPressedByName(name = "btn_fwd")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page < getPages()[-1]:
						page += 1
					else:
						page = 1
					redraw = True
				
				# If we pressed the left cursor key, or clicked on the left button, scroll one page left
				if (screen == "page") and ((sdl_event and (sdl_event.key.keysym.sym == SDLK_LEFT)) or (clicked == "btn_back")):
					button = window.boxPressedByName(name = "btn_back")
					renderPage(window, page = page, button_clicked = button, flash = True, power_mode = power_mode)
					if page > 1:
						page -= 1
					else:
						page = getPages()[-1]
					redraw = True
						
				#########################################
				#
				# End of all user-defined actions
				#
				#########################################
				
				ts_event = False
			
		######################################################
		#
		# Because of user input, OR if a screen left the state
		# as 'redraw = True', continue to redraw the current screen
		#
		######################################################
		if redraw:
			# Re-render the main device button page
			if screen == "page":
				# This redraws once and waits for input
				renderPage(window, page = page, button_clicked = button, flash = False, power_mode = power_mode)
				redraw = False
				
			# Re-render the status/sysinfo page
			if screen == "status":
				# This redraws continuously
				renderStatus(window, button_clicked = button, flash = False, power_mode = power_mode)
				
			# Re-render the power monitor page
			if screen == "monitor":
				# This redraws continuously
				renderPowerMon(window, button_clicked = button, flash = False, power_mode = power_mode)
			
			# Flush updated screen buffer to display
			window.update(transition = transition)
	
	# Stop radio
	if energenie['lib']:
		logger.info("Shutting down energenie library")
		energenie['lib'].finished()
	
	# Stop touchscreen
	if ts:
		logger.info("Shutting down touchscreen library")
		ts.stop()
	
	# Clean up the SDL and TTF libraries
	logger.info("Shutting down SDL library")
	gfxClose()
		
	# Finally exit the application
	return 0
	
if __name__ == '__main__':
	sys.exit(sdlRFController())
