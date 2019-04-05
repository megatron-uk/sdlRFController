#!/usr/bin/env python3

# sdl_basics.py, Handy low level SDL initialisation functions using PySDL2
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
from sdl2 import *
from sdl2.sdlttf import *

from lib import config
from lib.newlog import newlog

# SDL routines
from sdl2 import *

# Set up a logger for this file
logger = newlog(__file__)

class gfxData():
	""" Encapsulation of an SDL window/canvas and a hardware dependent renderer """
	
	def __init__(self, window, renderer):
		self.window = window
		self.renderer = renderer
		self.surface = SDL_GetWindowSurface(self.window)
		self.backbuffer = SDL_CreateRGBSurface(0, config.SCREEN_W, config.SCREEN_H, config.SCREEN_BPP,
                                  0,
                                  0,
                                  0,
                                  255)
		self.old_backbuffer = SDL_CreateRGBSurface(0, config.SCREEN_W, config.SCREEN_H, config.SCREEN_BPP,
                                  0,
                                  0,
                                  0,
                                  255)
		self.render_texture = None
		
		# Boxes is a list of UI elements and their coordinates (x1,y1 - x2, y2) that can be clicked on or touched.
		# List refreshed each redraw of the screen and checked each time the SDL input event detects mouse click.
		# List is populated by each relevant function that draws an element on the screen.
		self.boxes = []
		
		self.mouse_x = ctypes.c_int(0)
		self.mouse_y = ctypes.c_int(0)
		self.mouse_buttons = False
		
	
	def mouseRead(self):
		self.mouse_buttons = SDL_GetMouseState(self.mouse_x, self.mouse_y)
		logger.debug("Coordinates x:%s y:%s" % (self.mouse_x.value, self.mouse_y.value))
	
	def boxPressed(self):
		for box in self.boxes:
			if (self.mouse_x.value >= box["x1"]) and (self.mouse_x.value <= box["x2"]):
				if (self.mouse_y.value >= box["y1"]) and (self.mouse_y.value <= box["y2"]):
					logger.debug("Button")
					return box["name"]
		return False
	
	def update(self, transition = None):
		""" Redraw the screen """		
		
		if transition is None:	
			# Without any transitions, just copy backbuffers, then render to texture
			self.render_texture = SDL_CreateTextureFromSurface(self.renderer, self.backbuffer)
			SDL_RenderCopy(self.renderer, self.render_texture, None, None)
			SDL_RenderPresent(self.renderer)
			SDL_DestroyTexture(self.render_texture)
		else:
			if transition == "FADE":
				GuiTransitionFadeOutIn(self)
			elif transition == "SLIDEL":
				GuiTransitionSlideOutIn(self, direction = "LEFT")
			elif transition == "SLIDER":
				GuiTransitionSlideOutIn(self, direction = "RIGHT")
			else:
				# Unsupported render mode
				self.render_texture = SDL_CreateTextureFromSurface(self.renderer, self.backbuffer)
				SDL_RenderCopy(self.renderer, self.render_texture, None, None)
				SDL_RenderPresent(self.renderer)
				SDL_DestroyTexture(self.render_texture)
				
		# Lastly, take a copy of the old backbuffer (so we can do effects on it next time round)
		SDL_BlitSurface(self.backbuffer, None, self.old_backbuffer, None)
		#SDL_FillRect(self.backbuffer, None, config.BACKGROUND_COLOUR['r'], config.BACKGROUND_COLOUR['g'], config.BACKGROUND_COLOUR['b'])		
	
	def clear(self):
		""" Blank the screen """
		# Blank the UI element coordinates
		self.boxes = []
		
		SDL_FillRect(self.backbuffer, None, config.BACKGROUND_COLOUR['r'], config.BACKGROUND_COLOUR['g'], config.BACKGROUND_COLOUR['b'])

	def sdlWindow(self):
		return self.window
		
	def sdlRenderer(self):
		return self.renderer
		
	def sdlSurface(self):
		return self.buffer_2

class GarbageCleaner():
	""" Capture and clean up sdl surfaces, textures and images """
	
	def __init__(self):
		self.textures = []
		self.surfaces = []
		self.fonts = []
		
	def regS(self, surface):
		self.surfaces.append(surface)
		
	def regT(self, texture):
		self.textures.append(texture)
		
	def regF(self, font):
		self.fonts.append(font)
		
	def cleanUp(self):
		for t in self.textures:
			SDL_DestroyTexture(t)
		for s in self.surfaces:
			SDL_FreeSurface(s)
		for f in self.fonts:
			TTF_CloseFont(f)

def gfxInit():
	""" Initialise the SDL library for the configured screen mode """
	
	logger.info("Initialising libSDL for %sx%s" % (config.SCREEN_W, config.SCREEN_H))
	try:
		SDL_Init(SDL_INIT_VIDEO)
		
		mode = SDL_DisplayMode()
		driver_name = SDL_GetCurrentVideoDriver()
		if driver_name:
			logger.info("SDL Driver type is %s" % bytes.decode(driver_name))
			logger.debug("Checking available display modes...")
			num_modes = SDL_GetNumDisplayModes(0)
			for i in range(0, num_modes):
				current_mode = SDL_GetDisplayMode(0, i, mode)
				logger.debug("Mode - %sx%s @ %sHz" % (mode.w, mode.h, mode.refresh_rate))
		else:
			logger.error("Unable to initialise an SDL driver")
			logger.warn("Check the environment variable SDL_VIDEODRIVER for an incorrect/unavailable driver type")
			return False
		
		# Create a fixed sized graphisc window
		logger.info("Creating SDL window")
		window = SDL_CreateWindow(str.encode(config.APPLICATION_NAME), 
			SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED,
			config.SCREEN_W, 
			config.SCREEN_H, 
			(SDL_WINDOW_SHOWN)
		)
		
		# Get the details of the window that was created
		SDL_GetWindowDisplayMode(window, mode)
		logger.info("Created window is: %sx%s @ %sHz" % (mode.w, mode.h, mode.refresh_rate))
		
		# Create a renderer to draw into the window
		renderer = SDL_CreateRenderer(window, -1, 0, SDL_RENDERER_ACCELERATED);
		logger.info("Renderer created")
		
		# Combine window and renderer into a data structure that we then hand back to main code
		sdlWindowData = gfxData(window = window, renderer = renderer)
		
		# Initialise font engine
		TTF_Init()
		
		# Hide mouse cursor
		#SDL_ShowCursor(SDL_DISABLE)
		
		return sdlWindowData
	except Exception as e:
		logger.error("Unable to create SDL display")
		logger.error(e)
		return False
	
def gfxClose():
	SDL_ShowCursor(SDL_DISABLE)
	SDL_Quit()
	
def gfxSplashScreen(window = None):
	""" Fade in the loading splash screen """
	
	logger.info("Loading splash screen")
	
	g = GarbageCleaner()
	
	# Load splash bitmap and convert to texture
	image_surface = SDL_LoadBMP(str.encode(config.ASSETS['splash']))
	g.regS(image_surface)
	
	# Copy texture to display
	SDL_BlitSurface(image_surface, None, window.backbuffer, None)
	
	# Destroy SDL surface
	g.cleanUp()
	
	return True
	
def gfxPage(window = None, page = 1):
	""" Display a page of clickable buttons """
	
	logger.info("Loading page %s" % page)
	
	g = GarbageCleaner()
	window.clear()
	
	pages = list(config.SCREENS.keys())
	if page not in pages:
		page = 1
	logger.info("Page %s" % page)
	
	# Load generic button bitmap
	btn_surface = SDL_LoadBMP(str.encode(config.ASSETS['btn_default']))
	g.regS(btn_surface)
	
	# Try to load the button configuration for this page
	
	y_pos = 5
	x_left = 5
	x_right = config.SCREEN_W - ((2 * x_left) + config.BUTTON_WIDTH)
	for alignment in config.SCREENS[page]['BUTTON'].keys():
		
		y_pos = 5
		
		button_numbers = list(config.SCREENS[page]['BUTTON'][alignment].keys())
		for button_number in button_numbers:
			button = config.SCREENS[page]['BUTTON'][alignment][button_number]
			logger.info("Button %s.%s" % (page, button_number))
	
			# Left
			if alignment == "L":
				x_pos = x_left
			
			# Right
			if alignment == "R":
				x_pos = x_right
				
			# Is there a bitmap for this button?
			if button['image'] and os.path.exists(config.ASSETS_FOLDER + button['image']):
				new_btn_surface = SDL_LoadBMP(str.encode(config.ASSETS_FOLDER + button['image']))
				g.regS(new_btn_surface)
				blit_button = new_btn_surface
				btn_rect = SDL_Rect(x_pos, y_pos, blit_button.contents.w, blit_button.contents.h)
				SDL_BlitSurface(blit_button, None, window.backbuffer, btn_rect)
			else:
				# Display text instead of image
				blit_button = btn_surface
				btn_rect = SDL_Rect(x_pos, y_pos, blit_button.contents.w, blit_button.contents.h)
				SDL_BlitSurface(blit_button, None, window.backbuffer, btn_rect)	
			
			y_pos += config.BUTTON_HEIGHT + 5

	g.cleanUp()
	
	return page