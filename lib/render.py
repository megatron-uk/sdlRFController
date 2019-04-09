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
import psutil
from sdl2 import *
from sdl2.sdlttf import *

from lib import config
from lib.newlog import newlog
from lib.buttons import getPages, getButtons
from lib.gfx import GarbageCleaner, gfxLoadBMP, gfxGetText, gfxGetFont

# SDL routines
from sdl2 import *

# Set up a logger for this file
logger = newlog(__file__)

def renderButtonBar(window = None, button_clicked = None, flash = False, power_mode = "ON"):
	""" Display the navigation / button bar along the bottom of the screen - common to all screens """
	
	logger.debug("Loading button bar")
	g = GarbageCleaner()
	
	# Load generic button bitmaps
	btn_surface = gfxLoadBMP(window, config.ASSETS['btn_default'])
	btn_config = gfxLoadBMP(window, config.ASSETS['btn_config'])
	btn_back = gfxLoadBMP(window, config.ASSETS['btn_back'])
	btn_fwd =  gfxLoadBMP(window, config.ASSETS['btn_fwd'])
	
	# Power state indicator
	if power_mode == "ON":
		btn_power =  gfxLoadBMP(window, config.ASSETS['power_on'])
		btn_power_image = config.ASSETS['power_on']
	if power_mode == "OFF":
		btn_power =  gfxLoadBMP(window, config.ASSETS['power_off'])
		btn_power_image = config.ASSETS['power_off']
	
	# Splat the back nav buttons at the bottom
	x_pos = 5
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
	
	# Splat the forward nav buttons at the bottom
	x_pos = config.SCREEN_W - (btn_fwd.contents.w +5)
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
	
	# Splat the power mode buttons at the bottom
	x_pos = int(config.SCREEN_W / 2) - int(btn_power.contents.w / 2)
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
	
	# Splat the config/status buttons at the bottom
	x_pos = x_pos + btn_power.contents.w + 5 # previous button, plus an offset
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
	
	g.cleanUp()
	
	return True

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
	
	text_surface = gfxGetText(window, font, config.FONT_INFO_PT, font_colour, config.FONT_INFO_COLOUR, "IP: 192.168.1.1")
	x_pos = 0
	y_pos = 0
	btn_rect = SDL_Rect(x_pos, y_pos, text_surface.contents.w, text_surface.contents.h)
	SDL_BlitSurface(text_surface, None, window.backbuffer, btn_rect)
	
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
			logger.debug("Button %s.%s.%s:%s" % (page, button['align'], button['number'], button['text']))
	
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