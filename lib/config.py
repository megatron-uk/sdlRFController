APPLICATION_NAME = "sdlRFController"

# Time between screen refresh/event checks
REFRESH_TIME = 0.05

# Amount of time (in terms of screen refreshes) until we drop all cached
# surfaces and fonts and reload them again
CACHE_CLEAR_TIME = 100

# Enable more verbose output
DEBUG = 1
INFO = 1

# Screen size
SCREEN_W = 480
SCREEN_H = 320
SCREEN_BPP = 16
SCREEN_HIDE_MOUSE = 0

# Popup window size and location
SCREEN_POPUP_W = int(SCREEN_W * (2/3))
SCREEN_POPUP_H = int(SCREEN_H * (2/3))
SCREEN_POPUP_X = int((SCREEN_W - SCREEN_POPUP_W) / 2)
SCREEN_POPUP_Y = int((SCREEN_H - SCREEN_POPUP_H) / 2)

# Touchscreen calibration - my Waveshare 3.5 has swapped axis - x == y
TOUCH = {
	'axis_reversed' : True,
	'y_min' 	: 3880,
	'y_max' 	: 250,
	'x_min' 	: 300,
	'x_max' 	: 3880,
}

# Default screen fill
BACKGROUND_COLOUR = {
        'r'     : 0,
        'g'     : 0,
        'b'     : 0,
}
# Highlight colour
HIGHLIGHT_COLOUR = {
        'r'     : 180,
        'g'     : 180,
        'b'     : 180,
}

# Image folder
ASSETS_FOLDER = "./assets/"

# Flat graphics assets
ASSETS = {
        'splash' 		: ASSETS_FOLDER + 'splash.bmp', 
        'power_on'		: ASSETS_FOLDER + 'power_on2.bmp',
        'power_off'		: ASSETS_FOLDER + 'power_off.bmp',
        'btn_config'	: ASSETS_FOLDER + 'btn_config.bmp',
        'btn_restart'	: ASSETS_FOLDER + 'btn_restart.bmp',
        'btn_default'	: ASSETS_FOLDER + 'btn_default.bmp',
        'btn_fwd'		: ASSETS_FOLDER + 'btn_default_fwd2.bmp',
        'btn_back'		: ASSETS_FOLDER + 'btn_default_back2.bmp',
        'btn_confirm'	: ASSETS_FOLDER + 'btn_confirm.bmp',
        'btn_cancel'	: ASSETS_FOLDER + 'btn_cancel.bmp',
        'btn_meter'		: ASSETS_FOLDER + 'btn_meter.bmp',
        'btn_graph'		: ASSETS_FOLDER + 'btn_graph.bmp',
        'btn_graph_numbers'	: ASSETS_FOLDER + 'btn_graph_numbers.bmp',
        'btn_graph_volts'	: ASSETS_FOLDER + 'btn_graph_volts.bmp',
        'btn_graph_watt'	: ASSETS_FOLDER + 'btn_graph_watt.bmp',
        'btn_graph_hz'		: ASSETS_FOLDER + 'btn_graph_hz.bmp',
        'btn_graph_amp'		: ASSETS_FOLDER + 'btn_graph_amp.bmp',
}

# Font files
FONT_NORMAL = ASSETS_FOLDER + "verdana.ttf"
FONT_NORMAL_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_NORMAL_PT = 28

FONT_BUTTON = ASSETS_FOLDER + "verdanab.ttf"
FONT_BUTTON_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_BUTTON_PT = 28

FONT_MONITOR = ASSETS_FOLDER + "verdanab.ttf"
FONT_MONITOR_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_MONITOR_PT = 20

FONT_INFO = ASSETS_FOLDER + "verdana.ttf"
FONT_INFO_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_INFO_PT = 18

FONT_INFO_HEADER = ASSETS_FOLDER + "verdanab.ttf"
FONT_INFO_HEADER_COLOUR = { 'r' : 0, 'g': 0, 'b': 0}
FONT_INFO_HEADER_PT = 18

# Screen layout and configuration
MAX_ROWS = 5
MAX_COLS = 2

# Images used for button graphics should be this size
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

# How long a button flashes
BUTTON_FLASH_DELAY = 0.1

# How long between presses a button will respond to touchscreen
BUTTON_BOUNCE_TIME = 0.4

# A structure defining which buttons should be on which pages
SCREENS = {
	# First page
	1 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "MT-32",
					'image'	: "btn_mt32.bmp",
					'poweron' : [
						{'remote' : 0xA0001, 'socket' : 1, 'action' : "ON"},	# Turn this remote socket on
						{'tags' : ["midi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},			# Turn on any device with a tag of 'speakers'
					],
					'poweroff' : [
						{'remote' : 0xA0001, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0xA0001,
					'socket'	: 1,
					'tags'	: ["midi"],
				},
				2 : {
					'text'	: "SC-8820",
					'image'	: "btn_sc8820.bmp",
					'poweron'	: [
						{'remote' : 0xA0001, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["midi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0001, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0001,
					'socket'	: 3,
					'tags'	: ["midi"],
				},
				3 : {
					'text'	: "SC-55",
					'image'	: "btn_sc55.bmp",
					'poweron'	: [
						{'remote' : 0xA0001, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["midi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0001, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA0001,
					'socket'	: 2,
					'tags'	: ["midi"],
				},
				4 : {
					'text'	: "MIDI Switch",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0xA0001, 'socket' : 4, 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0001, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA0001,
					'socket'	: 4,
					'tags'	: ["midi sink"],
				},
			},
			'R' : {
				1 : {
					'text'	: "Dreamcast",
					'image'	: "btn_dreamcast.bmp",
					'poweron'	: [
						{'remote' : 0xA0008, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0008, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA0008,
					'socket'	: 4,
					'tags'	: [],
				},
				2 : {
					'text'	: "Saturn",
					'image'	: "btn_saturn.bmp",
					'poweron'	: [
						{'remote' : 0xA0002, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0002, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA0002,
					'socket'	: 4,
					'tags'	: [],
				},
				3 : {
					'text'	: "Master System",
					'image'	: "btn_sms.bmp",
					'poweron'	: [
						{'remote' : 0xA000A, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000A, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA000A,
					'socket'	: 2,
					'tags'	: [],
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: "btn_megadrive.bmp",
					'poweron'	: [
						{'remote' : 0xA000A, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000A, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA000A,
					'socket'	: 4,
					'tags'	: [],
				},
			},
		},
	},
	# Second page
	2 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "Playstation",
					'image'	: "btn_playstation.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Playstation 2",
					'image'	: "btn_playstation2.bmp",
					'poweron'	: [
						{'remote' : 0xA0007, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0007, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA0007,
					'socket'	: 4,
					'tags'	: [],
				},
				3 : {
					'text'	: "Playstation 3",
					'image'	: "btn_playstation3.bmp",
					'poweron'	: [
						{'remote' : 0xA0007, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0007, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA0007,
					'socket'	: 2,
					'tags'	: [],
				},
				4 : {
					'text'	: "Playstation 4",
					'image'	: "btn_playstation4.bmp",
					'poweron'	: [
						{'remote' : 0xA0007, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0007, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0007,
					'socket'	: 3,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Vita",
					'image'	: "btn_playstationtv.bmp",
					'poweron'	: [
						{'remote' : 0xA0009, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0009, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA0009,
					'socket'	: 2,
					'tags'	: [],
				},
				2 : {
					'text'	: "XBox",
					'image'	: "btn_xbox.bmp",
					'poweron'	: [
						{'remote' : 0xA0007, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0007, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0xA0007,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Xbox 360",
					'image'	: "btn_xbox360.bmp",
					'poweron'	: [
						{'remote' : 0xA0008, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0008, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0008,
					'socket'	: 3,
					'tags'	: [],
				},
			},
		},
	},
	# Third page
	3 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "PC-Engine",
					'image'	: "btn_pcengine.bmp",
					'poweron'	: [
						{'remote' : 0xA000A, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000A, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA000A,
					'socket'	: 3,
					'tags'	: [],
				},
				2 : {
					'text'	: "Turbo Duo",
					'image'	: "btn_pcenginecd.bmp",
					'poweron'	: [
						{'remote' : 0xA0002, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0002, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0002,
					'socket'	: 3,
					'tags'	: [],
				},
				3 : {
					'text'	: "ZX Spectrum",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0xA000B, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000B, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA000B,
					'socket'	: 2,
					'tags'	: [],
				},
				4 : {
					'text'	: "MSX",
					'image'	: "btn_msx.bmp",
					'poweron'	: [
						{'remote' : 0xA000B, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},		# Needed for keyboard/mouse switch
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000B, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA000B,
					'socket'	: 3,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Amiga 500",
					'image'	: "btn_amiga500.bmp",
					'poweron'	: [
						{'remote' : 0xA000B, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},		# Needed for keyboard/mouse switch
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000B, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0xA000B,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Amiga 1200",
					'image'	: "btn_amiga1200.bmp",
					'poweron'	: [
						{'remote' : 0xA0006, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},		# Needed for keyboard/mouse switch
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0006, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0xA0006,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Amstrad CPC",
					'image'	: "btn_amstradcpc.bmp",
					'poweron'	: [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "Atari ST",
					'image'	: "btn_atarist.bmp",
					'poweron'	: [
						{'remote' : 0xA000B, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},		# Needed for keyboard/mouse switch
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000B, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA000B,
					'socket'	: 4,
					'tags'	: [],
				},
			},
		},
	},
	# Fourth page
	4 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "PC-9821",
					'image'	: "btn_pc9821.bmp",
					'poweron'	: [
						{'remote' : 0xA0006, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio selector"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0006, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0006,
					'socket'	: 3,
					'tags'	: [],
				},
				2 : {
					'text'	: "Mac IICi",
					'image'	: "btn_maciici.bmp",
					'poweron'	: [
						{'remote' : 0xA0006, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio selector"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0006, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA0006,
					'socket'	: 2,
					'tags'	: [],
				},
				3 : {
					'text'	: "Risc PC 700",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0xA0006, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["vga sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio selector"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0006, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'	: 0xA0006,
					'socket'	: 4,
					'tags'	: [],
				},
				4 : {
					'text'	: "BBC Micro",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0xA0009, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0009, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0009,
					'socket'	: 3,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Gamecube",
					'image'	: "btn_gamecube.bmp",
					'poweron'	: [
						{'remote' : 0xA0002, 'socket' : 2, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0002, 'socket' : 2, 'action' : "OFF"},
					],
					'remote'	: 0xA0002,
					'socket'	: 2,
					'tags'	: [],
				},
				2 : {
					'text'	: "SNES",
					'image'	: "btn_snes.bmp",
					'poweron'	: [
						{'remote' : 0xA000A, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA000A, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0xA000A,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "NeoGeo AES",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "Atari Jaguar",
					'image'	: "btn_atarijaguar.bmp",
					'poweron'	: [
						{'remote' : 0xA0002, 'socket' : 1, 'action' : "ON"},
						{'tags' : ["scart sink"], 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'	: [
						{'remote' : 0xA0002, 'socket' : 1, 'action' : "OFF"},
					],
					'remote'	: 0xA0002,
					'socket'	: 1,
					'tags'	: [],	
				}
			},
		},
	},
	# Page 5
	5 : {
		'BUTTON' : {
			'L' : {
				1 : {
					'text' : "Monitor",
					'image': None,
					'poweron'   : [],
					'poweroff'  : [],
					'remote'    : 0xA0005,
					'socket'    : 2,
					'tags'  : ["hdmi sink", "vga sink", "scart sink"],
				},
				2 : {
					'text' : "Scart Switch",
					'image': None,
					'poweron'   : [
						{'remote' : 0xA0005, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'  : [
						{'remote' : 0xA0005, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'    : 0xA0005,
					'socket'    : 3,
					'tags'  : ["scart sink"],
				},
				3 : {
					'text' : "OSSC Scaler",
					'image': None,
					'poweron'   : [
						{'remote' : 0xA0005, 'socket' : 4, 'action' : "ON"},
						{'tags' : ["hdmi sink"], 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},
					],
					'poweroff'  : [
						{'remote' : 0xA0005, 'socket' : 4, 'action' : "OFF"},
					],
					'remote'    : 0xA0005,
					'socket'    : 4,
					'tags'  : ["scart sink", "vga sink"],
				},
				4 : {
					'text'	: "Audio Switch",
					'image'	: None,
					'poweron'	: [
						{'remote' : 0xA0004, 'socket' : 3, 'action' : "ON"},
						{'tags' : ["audio sink"], 'action' : "ON"},	
					],
					'poweroff'	: [
						{'remote' : 0xA0004, 'socket' : 3, 'action' : "OFF"},
					],
					'remote'	: 0xA0004,
					'socket'	: 3,
					'tags'	: ["audio selector"],
				},
			},
			'R' : {
				1 : {
					'text'	: "HDMI KVM",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0xA0009,
					'socket'	: 1,
					'tags'	: ["hdmi sink"],
				},
				2 : {
					'text'	: "VGA KVM",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0xA000D,
					'socket'	: 1,
					'tags'	: ["vga sink"],
				},
				3 : {
					'text'	: "Speakers",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0xA0005,
					'socket'	: 1,
					'tags'	: ["audio sink"],
				},
				4 : {
					'text'	: "Mixer",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0xA0008,
					'socket'	: 2,
					'tags'	: ["audio sink"],
				},
			}
		}
	},
	6 : {
		'BUTTON' : {
			'L' : {
				1 : {
					'text' : "Lamp",
					'image': None,
					'poweron'   : [],
					'poweroff'  : [],
					'remote'    : 0xA0004,
					'socket'    : 2,
					'tags'  : [],
				},
				2 : {
					'text' : "Disk Caddy",
					'image': None,
					'poweron'   : [],
					'poweroff'  : [],
					'remote'    : 0xA0004,
					'socket'    : 1,
					'tags'  : [],
				},
			},
                        'R' : {

                        },
		},
	},
}

# A list of any power monitor devices (MIHO004) that we can listen for
# broadcast signals from, to get the current power draw. This data can
# be viewed on the power monitor screen ('p' on the keyboard, or the 
# 'meter/gauge' button).
#
# NOte that we use the string based name in the energenie registry.kvs file
# as the device name...
POWER_MONITORS = {
	1 : {
		'text' 		: "Wall socket 1",
		'deviceid'	: 'mon1',
	},
	2 : {
		'text' 		: "Wall socket 2",
		'deviceid'	: 'mon2',
	},
	3 : {
		'text' 		: "Wall socket 3",
		'deviceid'	: 'mon3',
	},
	4 : {
		'text' 		: "Wall socket 4",
		'deviceid'	: 'mon4',
	},
}
