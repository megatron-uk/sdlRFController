#!/usr/bin/env python3

# render.py, Render output screens for sdlRFController
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
import ctypes
import time
import datetime
import psutil
from sdl2 import *
from sdl2.sdlttf import *

from lib import config
from lib.newlog import newlog
from lib.buttons import getPages, getButtons
from lib.gfx import GarbageCleaner, gfxLoadBMP, gfxGetText, gfxGetFont

# SDL routines
import sdl2
from sdl2 import *

# Set up a logger for this file
logger = newlog(__file__)

def renderFlash(window = None, page = None, button_clicked = None, power_mode = "ON", screen = None, energenie = None, graph_mode = None):
	""" Flash a button on a page """
	
	if screen == "page":
		renderPage(window, page = page, button_clicked = button_clicked, flash = True, power_mode = power_mode)
	if screen == "status":
		renderStatus(window, button_clicked = button_clicked, flash = True, power_mode = power_mode)
	if screen == "monitor":
		renderPowerMon(window, page = page, button_clicked = button_clicked, flash = True, power_mode = power_mode, energenie = energenie, graph_mode = graph_mode)
	window.update()
	
	return True

def renderButtonBar(window = None, button_clicked = None, flash = False, power_mode = "ON"):
	""" Display the navigation / button bar along the bottom of the screen - common to all screens """
	
	logger.debug("Loading button bar")
	g = GarbageCleaner()
	
	# Load generic button bitmaps
	btn_surface = gfxLoadBMP(window, config.ASSETS['btn_default'])
	btn_restart = gfxLoadBMP(window, config.ASSETS['btn_restart'])
	btn_config = gfxLoadBMP(window, config.ASSETS['btn_config'])
	btn_back = gfxLoadBMP(window, config.ASSETS['btn_back'])
	btn_fwd =  gfxLoadBMP(window, config.ASSETS['btn_fwd'])
	btn_meter =  gfxLoadBMP(window, config.ASSETS['btn_meter'])
	
	# Power state indicator
	if power_mode == "ON":
		btn_power =  gfxLoadBMP(window, config.ASSETS['power_on'])
		btn_power_image = config.ASSETS['power_on']
	if power_mode == "OFF":
		btn_power =  gfxLoadBMP(window, config.ASSETS['power_off'])
		btn_power_image = config.ASSETS['power_off']
	
	x_spacing = 5
	
	# Splat the back nav buttons at the bottom
	x_pos = x_spacing
	y_pos = config.SCREEN_H - btn_back.contents.h
	back_rect = SDL_Rect(x_pos, y_pos, btn_back.contents.w, btn_back.contents.h)
	SDL_BlitSurface(btn_back, None, window.backbuffer, back_rect)
	# Register nav buttons as available on the page for clicks
	button = {}
	button['name'] = "btn_back"
	button['image'] =  config.ASSETS['btn_back']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_back.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_back.contents.h
	window.boxes.append(button)
	
	# Put the power meter button at the bottom
	x_pos = x_pos + btn_meter.contents.w + x_spacing # previous button, plus an offset
	y_pos = config.SCREEN_H - btn_meter.contents.h
	meter_rect = SDL_Rect(x_pos, y_pos, btn_meter.contents.w, btn_meter.contents.h)
	SDL_BlitSurface(btn_meter, None, window.backbuffer, meter_rect)
	button = {}
	button['name'] = "btn_meter"
	button['image'] =  config.ASSETS['btn_meter']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_meter.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_meter.contents.h
	window.boxes.append(button)

	
	# Splat the config/status buttons at the bottom
	x_pos = x_pos + btn_power.contents.w + x_spacing # previous button, plus an offset
	y_pos = config.SCREEN_H - btn_config.contents.h
	config_rect = SDL_Rect(x_pos, y_pos, btn_config.contents.w, btn_config.contents.h)
	SDL_BlitSurface(btn_config, None, window.backbuffer, config_rect)
	button = {}
	button['name'] = "btn_config"
	button['image'] =  config.ASSETS['btn_config']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_config.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_config.contents.h
	window.boxes.append(button)
	
		# Splat the power mode buttons at the bottom
	x_pos = x_pos + btn_back.contents.w + x_spacing # previous button, plus an offset
	y_pos = config.SCREEN_H - btn_power.contents.h
	pow_rect = SDL_Rect(x_pos, y_pos, btn_power.contents.w, btn_power.contents.h)
	SDL_BlitSurface(btn_power, None, window.backbuffer, pow_rect)
	button = {}
	button['name'] = "btn_power"
	button['image'] =  btn_power_image
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_power.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_power.contents.h
	window.boxes.append(button)
	
	# Splat the restart buttons at the bottom
	x_pos = x_pos + btn_restart.contents.w + x_spacing # previous button, plus an offset
	y_pos = config.SCREEN_H - btn_restart.contents.h
	restart_rect = SDL_Rect(x_pos, y_pos, btn_restart.contents.w, btn_restart.contents.h)
	SDL_BlitSurface(btn_restart, None, window.backbuffer, restart_rect)
	button = {}
	button['name'] = "btn_restart"
	button['image'] =  config.ASSETS['btn_restart']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_restart.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_restart.contents.h
	window.boxes.append(button)
	
	# Splat the forward nav buttons at the bottom
	x_pos = x_pos + btn_fwd.contents.w + x_spacing # previous button, plus an offset
	y_pos = config.SCREEN_H - btn_fwd.contents.h
	fwd_rect = SDL_Rect(x_pos, y_pos, btn_fwd.contents.w, btn_back.contents.h)
	SDL_BlitSurface(btn_fwd, None, window.backbuffer, fwd_rect)
	# Register nav buttons as available on the page for clicks
	button = {}
	button['name'] = "btn_fwd"
	button['image'] =  config.ASSETS['btn_fwd']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_fwd.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_fwd.contents.h
	window.boxes.append(button)
	
	g.cleanUp()
	
	return True

def renderConfirmWindow(window = None, header = None, text = None):
	""" Show a semi-transparent overlay window with a Yes/No confirmation option """
	
	logger.debug("Loading confirmation window")
	
	logger.debug("%sx%s at x:%s y:%s" % (config.SCREEN_POPUP_W, config.SCREEN_POPUP_H, config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y))
	
	font_header = gfxGetFont(window, config.FONT_INFO_HEADER, config.FONT_INFO_HEADER_PT)
	font = gfxGetFont(window, config.FONT_INFO, config.FONT_INFO_PT)
	font_colour = pixels.SDL_Color(config.FONT_INFO_COLOUR['r'], config.FONT_INFO_COLOUR['g'], config.FONT_INFO_COLOUR['b'])
	font_reverse_colour = pixels.SDL_Color(config.FONT_INFO_HEADER_COLOUR['r'], config.FONT_INFO_HEADER_COLOUR['g'], config.FONT_INFO_HEADER_COLOUR['b'])
	
	g = GarbageCleaner()
	
	# Remove any existing buttons so that they cannot be clicked
	window.boxes = []
	
	# We don't call a window.clear() as we want to preserve what is shown below
	
	if (SDL_BYTEORDER == SDL_BIG_ENDIAN):
		rmask = 0xff000000
		gmask = 0x00ff0000
		bmask = 0x0000ff00
		amask = 0x000000ff
	else:
		rmask = 0x000000ff
		gmask = 0x0000ff00
		bmask = 0x00ff0000
		amask = 0xff000000
	
	# Create a surface with the alpha channel set
	driver_name = SDL_GetCurrentVideoDriver()
	if bytes.decode(driver_name) != "RPI":
		logger.debug("Using transparency overlay")
		overlay_surface = SDL_CreateRGBSurface(0, config.SCREEN_POPUP_W , config.SCREEN_POPUP_H, 32 , rmask , gmask , bmask , amask )
		g.regS(overlay_surface)
		overlay_rect = SDL_Rect(config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y, overlay_surface.contents.w, overlay_surface.contents.h)
		SDL_FillRect(overlay_surface, None , 0xBB0F0F0F) # ARGB format
		SDL_BlitSurface(overlay_surface, None, window.backbuffer, overlay_rect)
	else:
		logger.debug("Not using transparency with RPI driver")
		overlay_surface = SDL_CreateRGBSurface(0, config.SCREEN_POPUP_W , config.SCREEN_POPUP_H, config.SCREEN_BPP , 0 , 0 , 0 , 255 )
		g.regS(overlay_surface)
		overlay_rect = SDL_Rect(config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y, overlay_surface.contents.w, overlay_surface.contents.h)
		SDL_FillRect(overlay_surface, None , 0x00000000) # ARGB format
		SDL_BlitSurface(overlay_surface, None, window.backbuffer, overlay_rect)

	# Print the header in reverse text in the overlay box
	if header is not None:
		logger.info(header)
		header_text_surface = TTF_RenderText_Blended(font_header, str.encode(header), font_reverse_colour)
		g.regS(header_text_surface)
		header_rect = SDL_Rect(config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y, config.SCREEN_POPUP_W, header_text_surface.contents.h + 2)
		SDL_FillRect(window.backbuffer, header_rect, window.highlight_colour)
		header_text_rect = SDL_Rect(config.SCREEN_POPUP_X + int((config.SCREEN_POPUP_W - header_text_surface.contents.w) / 2), config.SCREEN_POPUP_Y + 2, header_text_surface.contents.w, header_text_surface.contents.h)
		SDL_BlitSurface(header_text_surface, None, window.backbuffer, header_text_rect)
		y_offset = header_text_surface.contents.h
	else:
		y_offset = 0

	# Print the text in the overlay box
	if text is not None:
		logger.info(text)
		text_surface = TTF_RenderText_Blended_Wrapped(font, str.encode(text), font_colour, config.SCREEN_POPUP_W - 4)
		g.regS(text_surface)
		overlay_rect = SDL_Rect(config.SCREEN_POPUP_X + 2, config.SCREEN_POPUP_Y + y_offset + 2, text_surface.contents.w, text_surface.contents.h)
		SDL_BlitSurface(text_surface, None, window.backbuffer, overlay_rect)
	
	# Add Yes/No buttons
	btn_confirm = gfxLoadBMP(window, config.ASSETS['btn_confirm'])
	btn_cancel = gfxLoadBMP(window, config.ASSETS['btn_cancel'])
	
	# Splat the confirm nav buttons at the bottom of the overlay
	x_pos = config.SCREEN_POPUP_X + 5
	y_pos = (config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H) - btn_confirm.contents.h - 5
	confirm_rect = SDL_Rect(x_pos, y_pos, btn_confirm.contents.w, btn_confirm.contents.h)
	SDL_BlitSurface(btn_confirm, None, window.backbuffer, confirm_rect)
	# Register nav buttons as available on the page for clicks
	button = {}
	button['name'] = "btn_confirm"
	button['image'] =  config.ASSETS['btn_confirm']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_confirm.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_confirm.contents.h
	window.boxes.append(button)
	
	# Splat the cancel nav buttons at the bottom of the overlay
	x_pos = ((x_pos + config.SCREEN_POPUP_W) - btn_cancel.contents.w) - 10
	y_pos = (config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H) - btn_cancel.contents.h - 5
	cancel_rect = SDL_Rect(x_pos, y_pos, btn_cancel.contents.w, btn_cancel.contents.h)
	SDL_BlitSurface(btn_cancel, None, window.backbuffer, cancel_rect)
	# Register nav buttons as available on the page for clicks
	button = {}
	button['name'] = "btn_cancel"
	button['image'] =  config.ASSETS['btn_cancel']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_cancel.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_cancel.contents.h
	window.boxes.append(button)
	
	window.update()
	time.sleep(0.1)
	
	if bytes.decode(driver_name) != "RPI":
		# Redraw on the existing renderer
		SDL_SetRenderDrawColor(window.renderer, config.HIGHLIGHT_COLOUR['r'], config.HIGHLIGHT_COLOUR['g'], config.HIGHLIGHT_COLOUR['b'], SDL_ALPHA_OPAQUE)
		SDL_RenderDrawLine(window.renderer, config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y, config.SCREEN_POPUP_X + config.SCREEN_POPUP_W, config.SCREEN_POPUP_Y);
		SDL_RenderDrawLine(window.renderer, config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H, config.SCREEN_POPUP_X + config.SCREEN_POPUP_W, config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H);
		SDL_RenderDrawLine(window.renderer, config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y, config.SCREEN_POPUP_X, config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H);
		SDL_RenderDrawLine(window.renderer, config.SCREEN_POPUP_X + config.SCREEN_POPUP_W, config.SCREEN_POPUP_Y, config.SCREEN_POPUP_X + config.SCREEN_POPUP_W, config.SCREEN_POPUP_Y + config.SCREEN_POPUP_H);
		window.update(reuse_texture = True)
	
	g.cleanUp()

def renderStatus(window = None, button_clicked = None, flash = False, power_mode = "ON"):
	""" Display system info / status """
	
	logger.debug("Loading status screen")
	
	g = GarbageCleaner()
	window.clear()
		
	# Render nav buttons
	renderButtonBar(window = window, button_clicked = button_clicked, flash = flash, power_mode = power_mode)
	
	# Load font
	font = gfxGetFont(window, config.FONT_INFO, config.FONT_INFO_PT)
	font_colour = pixels.SDL_Color(config.FONT_INFO_COLOUR['r'], config.FONT_INFO_COLOUR['g'], config.FONT_INFO_COLOUR['b'])
	
	################################################
	
	# Text start positions for column 0
	x_pos = 5
	y_pos = 5
	
	# Python version (a constant)
	text_python = "Python: %s.%s.%s" % (sys.version_info[0], sys.version_info[1], sys.version_info[2]) 
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, text_python)
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# PySDL2 version (a constant)
	text_pysdl_version = "PySDL2 Library: %s" % sdl2.__version__
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, text_pysdl_version)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# SDL version (a constant)
	text_sdl_version = "SDL Library: %s.%s.%s" % (sdl2.version.SDL_MAJOR_VERSION, sdl2.version.SDL_MINOR_VERSION, sdl2.version.SDL_PATCHLEVEL)
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, text_sdl_version)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# SDL Driver type (a constant)
	text_sdl_driver = "SDL Driver: %s" % bytes.decode(SDL_GetCurrentVideoDriver())
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, text_sdl_driver)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# SDL render display size
	x = ctypes.c_int(0)
	y = ctypes.c_int(0)
	SDL_GetWindowSize(window.window, x, y)
	text_window_bytes = "SDL Display: %sx%s" % (x.value, y.value)
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, text_window_bytes)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Surfaces cached in memory
	text_cached_surfaces = "Surfaces: %s" % len(window.cachedSurfaces.keys())
	text_surface = TTF_RenderText_Blended(font, str.encode(text_cached_surfaces), font_colour)
	g.regS(text_surface)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Fonts open
	text_cached_fonts = "Open Fonts: %s" % len(window.cachedFonts.keys())
	text_surface = TTF_RenderText_Blended(font, str.encode(text_cached_fonts), font_colour)
	g.regS(text_surface)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	################################################
	
	# Text start positions for column 1
	x_pos = int(config.SCREEN_W / 2) + 5
	y_pos = 5
	
	# IP Address
	na = psutil.net_if_addrs()
	ns = psutil.net_if_stats()
	text_ip = "IP: "
	text_surface = TTF_RenderText_Blended(font, str.encode(text_ip), font_colour)
	g.regS(text_surface)
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# CPU frequency
	cpu_speed = int(int(open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").read().split('\n')[0]) / 1000)
	text_cpu_speed = "CPU Speed: %s MHz" % cpu_speed
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_cpu_speed), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# CPU load
	text_cpu = "CPU Load: %3s%%" % int(psutil.cpu_percent(interval = (0.5))) 
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_cpu), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# CPU temp
	temp = int(int(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000)
	text_temp = "CPU Temp: %s C" % temp
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_temp), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Uptime
	ts = int(int(time.mktime(datetime.datetime.now().timetuple())) - psutil.boot_time())
	text_time = "Uptime: %s sec" % ts
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_time), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Current RAM use
	process = psutil.Process(os.getpid())
	text_memory_size = "Process: %s kbytes" % int(process.memory_info().rss / 1024)
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_memory_size), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Number of open files
	text_files = "Files: %s" % len(psutil.Process(os.getpid()).open_files())
	y_pos = y_pos + text_surface.contents.h + 5
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	text_surface = TTF_RenderText_Blended(font, str.encode(text_files), font_colour)
	g.regS(text_surface)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
	# Total clicks
	# Kernel ver	
	
	g.cleanUp()
	window.update()
	return True

def renderPage(window = None, page = 1, button_clicked = None, flash = False, power_mode = "ON"):
	""" Display a page of clickable buttons """
	
	logger.debug("Loading page %s" % page)
	
	g = GarbageCleaner()
	window.clear()
		
	# Render nav buttons
	renderButtonBar(window = window, button_clicked = button_clicked, flash = flash, power_mode = power_mode)
	
	btn_surface = gfxLoadBMP(window, config.ASSETS['btn_default'])
	
	# Load font
	font = gfxGetFont(window, config.FONT_BUTTON, config.FONT_BUTTON_PT)
	font_colour = pixels.SDL_Color(config.FONT_BUTTON_COLOUR['r'], config.FONT_BUTTON_COLOUR['g'], config.FONT_BUTTON_COLOUR['b'])
	
	# Try to load the button configuration for this page
	y_pos = 0
	x_left = 5
	x_right = config.SCREEN_W - ((2 * x_left) + config.BUTTON_WIDTH)
	for alignment in ["L", "R"]:
		
		y_pos = 0
		buttons = getButtons(page, alignment)
		for button in buttons:
			#logger.debug("Button %s.%s.%s:%s" % (page, button['align'], button['number'], button['text']))
	
			# Left
			if alignment == "L":
				x_pos = x_left
			
			# Right
			if alignment == "R":
				x_pos = x_right
				
			# Is there a bitmap for this button?
			if button['image'] and (os.path.exists(config.ASSETS_FOLDER + button['image'])):
				new_btn_surface = gfxLoadBMP(window, config.ASSETS_FOLDER + button['image'])
				blit_button = new_btn_surface
				btn_rect = SDL_Rect(x_pos, y_pos, blit_button.contents.w, blit_button.contents.h)
				SDL_BlitSurface(blit_button, None, window.backbuffer, btn_rect)
				
				# Register this button as available on the page for clicks
				button['name'] = "deviceClick"
				button['x1'] = x_pos
				button['x2'] = x_pos + blit_button.contents.w
				button['y1'] = y_pos
				button['y2'] = y_pos + blit_button.contents.h
				window.boxes.append(button)
			else:
				# Display default button
				blit_button = btn_surface
				btn_rect = SDL_Rect(x_pos, y_pos, blit_button.contents.w, blit_button.contents.h)
				SDL_BlitSurface(blit_button, None, window.backbuffer, btn_rect)
				
				# Register this button as available on the page for clicks
				button['name'] = "deviceClick"
				button['x1'] = x_pos
				button['x2'] = x_pos + blit_button.contents.w
				button['y1'] = y_pos
				button['y2'] = y_pos + blit_button.contents.h
				window.boxes.append(button)
				
				# Display text on button
				text_surface = gfxGetText(window, font, config.FONT_BUTTON_PT, font_colour, config.FONT_BUTTON_COLOUR, button['text'])
				btn_rect = SDL_Rect(x_pos + int((blit_button.contents.w - text_surface.contents.w) / 2), y_pos + int((blit_button.contents.h - text_surface.contents.h) / 2), text_surface.contents.w, text_surface.contents.h)
				SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
			
			y_pos += config.BUTTON_HEIGHT + 5

	# Are we flashing a clicked button?
	if flash and (button_clicked is not None):
		# Render standard screen
		window.update()
		
		# Turn clicked button a different colour
		select_rect = SDL_Rect(button_clicked['x1'], button_clicked['y1'], button_clicked['x2'] - button_clicked['x1'], button_clicked['y2'] - button_clicked['y1'])
		SDL_FillRect(window.backbuffer, select_rect, window.highlight_colour)

		# Re-render screen
		window.update()
		time.sleep(config.BUTTON_FLASH_DELAY)
		
		# Render standard button content again
		SDL_FillRect(window.backbuffer, select_rect, window.background_colour)
		
		# 1. We have an image:
		if button_clicked['image']:
			old_btn_surface = gfxLoadBMP(window, config.ASSETS_FOLDER + button_clicked['image'])
			SDL_BlitSurface(old_btn_surface, None, window.backbuffer, select_rect)
		
		else:
			# 2. We don't have an image - render text again
			SDL_BlitSurface(btn_surface, None, window.backbuffer, select_rect)
			text_surface = gfxGetText(window, font, config.FONT_BUTTON_PT, font_colour, config.FONT_BUTTON_COLOUR, button_clicked['text'])
			btn_rect = SDL_Rect(select_rect.x + int((select_rect.w - text_surface.contents.w) / 2), select_rect.y + int((select_rect.h - text_surface.contents.h) / 2), text_surface.contents.w, text_surface.contents.h)
			SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
		
	# 3.
	window.update()
	g.cleanUp()
	
	return page
	
def renderPowerMon(window = None, page = 1, button_clicked = None, flash = False, power_mode = "ON", energenie = None, graph_mode = None):
	""" Display a page of power consumption figures """
	
	logger.debug("Loading power monitor %s" % page)
	
	g = GarbageCleaner()
	window.clear()

	# Add the standard button bar
	renderButtonBar(window = window, button_clicked = button_clicked, flash = flash, power_mode = power_mode)

	# Add the graph option button bar
	btn_graph = gfxLoadBMP(window, config.ASSETS['btn_graph'])
	btn_graph_numbers = gfxLoadBMP(window, config.ASSETS['btn_graph_numbers'])
	btn_graph_watt = gfxLoadBMP(window, config.ASSETS['btn_graph_watt'])
	btn_graph_hz = gfxLoadBMP(window, config.ASSETS['btn_graph_hz'])
	btn_graph_volts = gfxLoadBMP(window, config.ASSETS['btn_graph_volts'])
	btn_graph_amp = gfxLoadBMP(window, config.ASSETS['btn_graph_amp'])

	# Place the graph option buttons above the main button bar at the bottom
	x_spacing = 5
	x_pos = x_spacing
	y_pos = config.SCREEN_H - (2 * btn_graph_numbers.contents.h) - 2
	graph_rect = SDL_Rect(x_pos, y_pos, btn_graph_numbers.contents.w, btn_graph_numbers.contents.h)
	SDL_BlitSurface(btn_graph_numbers, None, window.backbuffer, graph_rect)
	# Register nav buttons as available on the page for clicks
	button = {}
	button['name'] = "btn_graph_numbers"
	button['image'] =  config.ASSETS['btn_graph_numbers']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_graph_numbers.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_graph_numbers.contents.h
	window.boxes.append(button)

	x_pos = x_pos + btn_graph_numbers.contents.w + x_spacing # previous button, plus an offset
	meter_rect = SDL_Rect(x_pos, y_pos, btn_graph.contents.w, btn_graph.contents.h)
	SDL_BlitSurface(btn_graph, None, window.backbuffer, meter_rect)
	button = {}
	button['name'] = "btn_graph"
	button['image'] =  config.ASSETS['btn_graph']
	button['x1'] = x_pos
	button['x2'] = x_pos + btn_graph.contents.w
	button['y1'] = y_pos
	button['y2'] = y_pos + btn_graph.contents.h
	window.boxes.append(button)

	# Load graph buttons if in graph mode
	if graph_mode in ["btn_graph"]:
		x_pos = x_pos + btn_graph.contents.w + x_spacing # previous button, plus an offset
		meter_rect = SDL_Rect(x_pos, y_pos, btn_graph_volts.contents.w, btn_graph_volts.contents.h)
		SDL_BlitSurface(btn_graph_volts, None, window.backbuffer, meter_rect)
		button = {}
		button['name'] = "btn_graph_volts"
		button['image'] =  config.ASSETS['btn_graph_volts']
		button['x1'] = x_pos
		button['x2'] = x_pos + btn_graph_volts.contents.w
		button['y1'] = y_pos
		button['y2'] = y_pos + btn_graph_volts.contents.h
		window.boxes.append(button)
		
		x_pos = x_pos + btn_graph_numbers.contents.w + x_spacing # previous button, plus an offset
		meter_rect = SDL_Rect(x_pos, y_pos, btn_graph_hz.contents.w, btn_graph_hz.contents.h)
		SDL_BlitSurface(btn_graph_hz, None, window.backbuffer, meter_rect)
		button = {}
		button['name'] = "btn_graph_hz"
		button['image'] =  config.ASSETS['btn_graph_hz']
		button['x1'] = x_pos
		button['x2'] = x_pos + btn_graph_hz.contents.w
		button['y1'] = y_pos
		button['y2'] = y_pos + btn_graph_hz.contents.h
		window.boxes.append(button)
		
		x_pos = x_pos + btn_graph_hz.contents.w + x_spacing # previous button, plus an offset
		meter_rect = SDL_Rect(x_pos, y_pos, btn_graph_amp.contents.w, btn_graph_amp.contents.h)
		SDL_BlitSurface(btn_graph_amp, None, window.backbuffer, meter_rect)
		button = {}
		button['name'] = "btn_graph_amp"
		button['image'] =  config.ASSETS['btn_graph_amp']
		button['x1'] = x_pos
		button['x2'] = x_pos + btn_graph_amp.contents.w
		button['y1'] = y_pos
		button['y2'] = y_pos + btn_graph_amp.contents.h
		window.boxes.append(button)
		
		x_pos = x_pos + btn_graph_amp.contents.w + x_spacing # previous button, plus an offset
		meter_rect = SDL_Rect(x_pos, y_pos, btn_graph_watt.contents.w, btn_graph_watt.contents.h)
		SDL_BlitSurface(btn_graph_watt, None, window.backbuffer, meter_rect)
		button = {}
		button['name'] = "btn_graph_watt"
		button['image'] =  config.ASSETS['btn_graph_watt']
		button['x1'] = x_pos
		button['x2'] = x_pos + btn_graph_watt.contents.w
		button['y1'] = y_pos
		button['y2'] = y_pos + btn_graph_watt.contents.h
		window.boxes.append(button)

	# Load font
	font = gfxGetFont(window, config.FONT_MONITOR, config.FONT_MONITOR_PT)
	font_s = gfxGetFont(window, config.FONT_INFO, config.FONT_INFO_PT)
	font_colour = pixels.SDL_Color(config.FONT_MONITOR_COLOUR['r'], config.FONT_MONITOR_COLOUR['g'], config.FONT_MONITOR_COLOUR['b'])

	if graph_mode in [None, "btn_graph_numbers"]:

		#######################################
		#
		# Row for each sensor metric
		#
		#######################################
	
		col_width = int((config.SCREEN_W - 5)/ 5)
		y_start = 25
		y = y_start
		x_col0 = 5
		x_col1 = x_col0 + col_width + 5
	
		# voltage
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Voltage")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
		
		# frequency
		y = y + text_sensor_surface.contents.h + 5
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Hz")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
			
		# current
		y = y + text_sensor_surface.contents.h + 5
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Amps")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
			
		# apparent_power
		y = y + text_sensor_surface.contents.h + 5
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Apparent")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
			
		# reactive_power
		y = y + text_sensor_surface.contents.h + 5
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Reactive")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
			
		# real_power
		y = y + text_sensor_surface.contents.h + 5
		text_sensor_surface = gfxGetText(window, font_s, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "Real")
		text_rect = SDL_Rect(x_col0, y, text_sensor_surface.contents.w, text_sensor_surface.contents.h)
		SDL_BlitSurface(text_sensor_surface, None, window.backbuffer, text_rect)
		if (x_col0 + text_sensor_surface.contents.w) > x_col1:
			x_col1 = (x_col0 + text_sensor_surface.contents.w)
		
		###############################################
		#
		# Headers for each column of sensor monitor device
		#
		###############################################
		
		col_width = int((config.SCREEN_W - x_col1) / 4)
		x_col2 = x_col1 + col_width
		x_col3 = x_col2 + col_width
		x_col4 = x_col3 + col_width
		logger.debug("Column 1 starts at %s" % x_col1)
		y = 5
		text_surface = gfxGetText(window, font, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "A")
		text_rect = SDL_Rect(x_col1, y, text_surface.contents.w, text_surface.contents.h)
		SDL_BlitSurface(text_surface, None, window.backbuffer, text_rect)
		
		logger.debug("Column 2 starts at %s" % x_col2)
		y = 5
		text_surface = gfxGetText(window, font, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "B")
		text_rect = SDL_Rect(x_col2, y, text_surface.contents.w, text_surface.contents.h)
		SDL_BlitSurface(text_surface, None, window.backbuffer, text_rect)
	
		logger.debug("Column 3 starts at %s" % x_col3)
		y = 5
		text_surface = gfxGetText(window, font, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "C")
		text_rect = SDL_Rect(x_col3, y, text_surface.contents.w, text_surface.contents.h)
		SDL_BlitSurface(text_surface, None, window.backbuffer, text_rect)
	
		logger.debug("Column 4 starts at %s" % x_col4)
		y = 5
		text_surface = gfxGetText(window, font, config.FONT_MONITOR_PT, font_colour, config.FONT_MONITOR_COLOUR, "D")
		text_rect = SDL_Rect(x_col4, y, text_surface.contents.w, text_surface.contents.h)
		SDL_BlitSurface(text_surface, None, window.backbuffer, text_rect)
		
		##########################################
		#
		# Rows of sensor values for each column 
		# of sensor monitor device
		#
		##########################################
		
		x_col = x_col1
		if (energenie is not None) and ("monitors" in energenie.keys()):
			for power_monitor in energenie['monitors']:
				
				power = power_monitor.get_readings()
				if power.voltage != None:
					voltage = "%sv" % power.voltage
				else:
					voltage = "n/a"
					
				if power.frequency != None:
					frequency = "%2.1fHz" % power.frequency
				else:
					frequency = "n/a"
					
				current = "0" #% power.current
				apparent_power = "0" #% power.apparent_power
				
				if power.reactive_power != None:
					reactive_power = "%3.0fw" % power.reactive_power
				else:
					reactive_power = "n/a"
				
				if power.real_power != None:
					real_power = "%3.0fw" % power.real_power
				else:
					real_power = "n/a" #% power.real_power
				
				y = y_start
				
				for sensor in [voltage, frequency, current, apparent_power, reactive_power, real_power]:
				
					text_value_surface = TTF_RenderText_Blended(font_s, str.encode(str(sensor)), font_colour)
					g.regS(text_value_surface)
					text_value_rect = SDL_Rect(x_col, y, text_value_surface.contents.w, text_value_surface.contents.h)
					SDL_BlitSurface(text_value_surface, None, window.backbuffer, text_value_rect)
					
					y = y + text_sensor_surface.contents.h + 5
		
				x_col += col_width
			
	#elif graph is "":
	#	pass

	window.update()
	g.cleanUp()
	
	time.sleep(0.25)
	
	return True