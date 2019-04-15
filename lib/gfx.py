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

import gc
import os
import sys
import ctypes
import time
from sdl2 import *
from sdl2.sdlttf import *

from lib import config
from lib.newlog import newlog
from lib.buttons import getPages, getButtons

# SDL routines
from sdl2 import *

# Set up a logger for this file
logger = newlog(__file__)

class gfxData():
	""" Encapsulation of an SDL window/canvas and a hardware dependent renderer """
	
	def __init__(self, window, renderer):
		gc.enable()
		self.window = window
		self.renderer = renderer
		
		# We set up two surfaces so that we can do transition effects between the newly rendered screen
		# and the old one, if we choose to do so.
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
		
		# Cache of surfaces we've loaded from on-disk bitmaps
		self.cachedSurfaces = {}
		self.cachedFonts = {}
		
		# Store mouse/touchscreen coordinates
		self.mouse_x = ctypes.c_int(0)
		self.mouse_y = ctypes.c_int(0)
		self.mouse_buttons = False
		
		# Touchscreen raw values
		self.touch_y_raw = 0
		self.touch_x_raw = 0
		
		if config.TOUCH['axis_reversed']:
			if config.TOUCH['y_min'] > config.TOUCH['y_max']:
				self.touch_pts_per_xpixel = (config.SCREEN_W / abs(config.TOUCH['y_max'] - config.TOUCH['y_min']))
			else:
				self.touch_pts_per_xpixel = (config.SCREEN_W / abs(config.TOUCH['y_min'] - config.TOUCH['y_max']))
				
			if config.TOUCH['x_min'] > config.TOUCH['x_max']:
				self.touch_pts_per_ypixel = (config.SCREEN_H / abs(config.TOUCH['x_max'] - config.TOUCH['x_min']))
			else:
				self.touch_pts_per_ypixel = (config.SCREEN_H / abs(config.TOUCH['x_min'] - config.TOUCH['x_max']))
		
		else:
			if config.TOUCH['y_min'] > config.TOUCH['y_max']:
				self.touch_pts_per_ypixel = (config.SCREEN_W / abs(config.TOUCH['y_max'] - config.TOUCH['y_min']))
			else:
				self.touch_pts_per_ypixel = (config.SCREEN_W / abs(config.TOUCH['y_min'] - config.TOUCH['y_max']))
				
			if config.TOUCH['x_min'] > config.TOUCH['x_max']:
				self.touch_pts_per_xpixel = (config.SCREEN_H / abs(config.TOUCH['x_max'] - config.TOUCH['x_min']))
			else:
				self.touch_pts_per_xpixel = (config.SCREEN_H / abs(config.TOUCH['x_min'] - config.TOUCH['x_max']))
		
		logger.info("Touchscreen, x pts/pixel: %s" % self.touch_pts_per_xpixel)
		logger.info("Touchscreen, y pts/pixel: %s" % self.touch_pts_per_ypixel)
		
		self.background_colour = SDL_MapRGB(self.backbuffer.contents.format, config.BACKGROUND_COLOUR['r'], config.BACKGROUND_COLOUR['g'], config.BACKGROUND_COLOUR['b'])
		self.highlight_colour = SDL_MapRGB(self.backbuffer.contents.format, config.HIGHLIGHT_COLOUR['r'], config.HIGHLIGHT_COLOUR['g'], config.HIGHLIGHT_COLOUR['b'])
	
	def clearCache(self):
		""" Free any cached surfaces or fonts """
		cachedSurfaces = list(self.cachedSurfaces.keys())
		cachedFonts = list(self.cachedFonts.keys())
			
		for s in cachedSurfaces:
			#logger.debug("Freeing old surface [%s]" % s)
			SDL_FreeSurface(self.cachedSurfaces[s])
		self.cachedSurfaces = {}
		
		for f in cachedFonts:
			#logger.debug("Freeing old font [%s]" % f)
			TTF_CloseFont(self.cachedFonts[f])
		self.cachedFonts = {}
		
		#logger.debug("Running Python garbage collection")
		gc.collect()
	
	def touchRead(self, ts_event):
		""" Called when a Linux /dev/input/touchscreen event is detected - read the raw x/y values and map to the screen resolution coordinates """
		
		
		logger.debug("Raw Coordinates x:%s y:%s" % (self.touch_x_raw, self.touch_y_raw))
		
		if config.TOUCH['y_min'] > config.TOUCH['y_max']:
			self.mouse_y.value = int((config.TOUCH['y_min'] - self.touch_y_raw) *  (self.touch_pts_per_ypixel))
		else:
			self.mouse_y.value = int((self.touch_y_raw - config.TOUCH['y_min']) *  (self.touch_pts_per_ypixel))
		if config.TOUCH['x_min'] > config.TOUCH['x_max']:
			self.mouse_x.value = int((config.TOUCH['x_min'] - self.touch_x_raw) *  (self.touch_pts_per_xpixel))
		else:
			self.mouse_x.value = int((self.touch_x_raw - config.TOUCH['x_min']) *  (self.touch_pts_per_xpixel))
		
		# Error correction - constrain to screen res
		if self.mouse_x.value < 0:
			self.mouse_x.value = 0
		
		if self.mouse_x.value > config.SCREEN_W:
			self.mouse_x.value = config.SCREEN_W
		
		if self.mouse_y.value < 0:
			self.mouse_y.value = 0
		
		if self.mouse_y.value > config.SCREEN_H:
			self.mouse_y.value = config.SCREEN_H
		
		logger.debug("Coordinates x:%s y:%s" % (self.mouse_x.value, self.mouse_y.value))
	
	def mouseRead(self, event):
		""" Called whenever an SDL Event of type touchscreen or mouse click is detected, reads and stores pointer position """
		self.mouse_buttons = SDL_GetMouseState(self.mouse_x, self.mouse_y)
		logger.debug("Coordinates x:%s y:%s" % (self.mouse_x.value, self.mouse_y.value))
		logger.debug("Clicks: %s" % event.button.clicks)
	
	def boxPressed(self):
		""" Compares the values of the current pointer position with any UI elements we've drawn on scree.
		If any areas have been clicked then the name of the UI element is returned and the main while-loop
		event handler can deal with it. """
		for box in self.boxes:
			if (self.mouse_x.value >= box["x1"]) and (self.mouse_x.value <= box["x2"]):
				if (self.mouse_y.value >= box["y1"]) and (self.mouse_y.value <= box["y2"]):
					logger.debug("Button")
					return box
		return False
	
	def boxPressedByName(self, name = None):
		""" Return a button from the list of current boxes, if it exists by name """
		for box in self.boxes:
			if box['name'] == name:
				return box
		return False
	
	def update(self, transition = None, reuse_texture = False):
		""" Redraw the screen """		
		
		# Without any transitions, just copy backbuffers, then render to texture
		if reuse_texture:
			SDL_RenderCopy(self.renderer, self.render_texture, None, None)
		else:
			self.render_texture = SDL_CreateTextureFromSurface(self.renderer, self.backbuffer)
			SDL_RenderCopy(self.renderer, self.render_texture, None, None)
		SDL_RenderPresent(self.renderer)
		SDL_DestroyTexture(self.render_texture)		
				
		# Lastly, take a copy of the old backbuffer (so we can do effects on it next time round)
		SDL_BlitSurface(self.backbuffer, None, self.old_backbuffer, None)
		
	def clear(self):
		""" Blank the screen - most likely called at the start of displaying any new page """
		# Blank the UI element coordinates
		self.boxes = []
		SDL_FillRect(self.backbuffer, None, self.background_colour)

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
			pass
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
		else:
			logger.error("Unable to initialise an SDL driver")
			logger.warn("Check the environment variable SDL_VIDEODRIVER for an incorrect/unavailable driver type")
			return False
		
		# Create a fixed sized graphics window
		logger.info("Creating SDL window")
		window = SDL_CreateWindow(str.encode(config.APPLICATION_NAME), 
			SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED,
			config.SCREEN_W, 
			config.SCREEN_H, 
			(SDL_WINDOW_SHOWN)
		)
		
		# Get the details of the window that was created
		#SDL_GetCurrentDisplayMode()
		#SDL_GetWindowDisplayMode(window, mode)
		num_displays = SDL_GetNumVideoDisplays()
		for i in range(0, SDL_GetNumVideoDisplays()):
			SDL_GetCurrentDisplayMode(i, mode)
			logger.info("Current physical display #%s: %sx%s @ %sHz" % (i, mode.w, mode.h, mode.refresh_rate))
		
		x = ctypes.c_int(0)
		y = ctypes.c_int(0)
		SDL_GetWindowSize(window, x, y)
		logger.info("Current window: %sx%s" % (x.value, y.value))
		
		if (x.value != config.SCREEN_W) or (y.value != config.SCREEN_H):
			logger.warn("Unable to create a window of the requested size")
		
		# Create a renderer to draw into the window
		renderer = SDL_CreateRenderer(window, -1, 0, SDL_RENDERER_ACCELERATED);
		logger.info("Renderer created")
		
		# Combine window and renderer into a data structure that we then hand back to main code
		sdlWindowData = gfxData(window = window, renderer = renderer)
		
		# Initialise font engine
		TTF_Init()
		
		# Hide mouse cursor
		SDL_ShowCursor(SDL_DISABLE)
		
		return sdlWindowData
	except Exception as e:
		logger.error("Unable to create SDL display")
		logger.error(e)
		return False
	
def gfxClose():
	""" Unload SDL """
	
	SDL_ShowCursor(SDL_DISABLE)
	TTF_Quit()
	SDL_Quit()
	
def gfxLoadBMP(window = None, filename = None):
	""" Load a bitmap file from disk, or from an already cached surface object """
	
	if filename in window.cachedSurfaces.keys():
		logger.debug("Surface cache hit for bitmap [%s]" % filename)
		surface = window.cachedSurfaces[filename]
		
	else:
		logger.debug("Loading bitmap from disk [%s]" % filename)
		surface = SDL_LoadBMP(str.encode(filename))
		window.cachedSurfaces[filename] = surface
	return surface

def gfxGetText(window, font, pt, sdl_colour, colour, text):
	""" Generate a text surface, or load from an already cached text surface object """
	
	k = str(font) + str(pt) + str(colour) + str(text)
	if k in window.cachedSurfaces.keys():
		logger.debug("Surface cache hit for text [%s:%s:%s:%s]" % (font, pt, str(colour), text))
		surface = window.cachedSurfaces[k]
	else:
		logger.debug("Generating text surface from string [%s]" % text)
		surface = TTF_RenderText_Blended(font, str.encode(text), sdl_colour)
		window.cachedSurfaces[k] = surface
	return surface

def gfxGetFont(window, font, pt):
	""" Load a font from disk, or from an already cached font object """
	
	k = str(font) + str(pt)
	if k in window.cachedFonts.keys():
		logger.debug("Font cache hit for font [%s:%s]" % (font, pt))
		font = window.cachedFonts[k]
	else:
		logger.debug("Loading font from disk [%s]" % font)
		font = TTF_OpenFont(str.encode(font), pt)
		window.cachedFonts[k] = font
	return font
	

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
	
