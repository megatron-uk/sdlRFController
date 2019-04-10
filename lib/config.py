APPLICATION_NAME = "sdlRFController"

# Time between screen refresh/event checks
REFRESH_TIME = 0.2

# Amount of time (in terms of screen refreshes) until we drop all cached
# surfaces and fonts and reload them again
CACHE_CLEAR_TIME = 10

# Enable more verbose output
DEBUG = 0
INFO = 1

# Screen size
SCREEN_W = 480
SCREEN_H = 320
SCREEN_BPP = 24

# Popup window size and location
SCREEN_POPUP_W = int(SCREEN_W * (2/3))
SCREEN_POPUP_H = int(SCREEN_H * (2/3))
SCREEN_POPUP_X = int((SCREEN_W - SCREEN_POPUP_W) / 2)
SCREEN_POPUP_Y = int((SCREEN_H - SCREEN_POPUP_H) / 2)

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
}

# Font files
FONT_NORMAL = ASSETS_FOLDER + "verdana.ttf"
FONT_NORMAL_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_NORMAL_PT = 28

FONT_BUTTON = ASSETS_FOLDER + "verdanab.ttf"
FONT_BUTTON_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_BUTTON_PT = 28

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
BUTTON_FLASH_DELAY = 0.2

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
						{'remote' : 0x0000, 'socket' : 1, 'action' : "ON"},	# Turn this remote socket on
						{'tags' : ["speakers"], 'action' : "ON"},			# Turn on any device with a tag of 'speakers'
					],
					'poweroff' : [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: ["midi"],
				},
				2 : {
					'text'	: "SC-8820",
					'image'	: "btn_sc8820.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: ["midi"],
				},
				3 : {
					'text'	: "SC-55",
					'image'	: "btn_sc55.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: ["midi"],
				},
				4 : {
					'text'	: "Mixer",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: ["speakers"],
				},
			},
			'R' : {
				1 : {
					'text'	: "Dreamcast",
					'image'	: "btn_dreamcast.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Saturn",
					'image'	: "btn_saturn.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Master System",
					'image'	: "btn_sms.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: "btn_megadrive.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
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
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Playstation 3",
					'image'	: "btn_playstation3.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "Playstation 4",
					'image'	: "btn_playstation4.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Vita",
					'image'	: "btn_playstationtv.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "XBox",
					'image'	: "btn_xbox.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Xbox 360",
					'image'	: "btn_xbox360.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
		},
	},
	# Second page
	3 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "PC-Engine",
					'image'	: "btn_pcengine.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Turbo Duo",
					'image'	: "btn_pcenginecd.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Atari Jaguar",
					'image'	: "btn_atarijaguar.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "MSX",
					'image'	: "btn_msx.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Amiga 500",
					'image'	: "btn_amiga500.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Amiga 1200",
					'image'	: "btn_amiga1200.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Amstrad CPC",
					'image'	: "btn_amstradcpc.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "Atari ST",
					'image'	: "btn_atarist.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
		},
	},
	# Second page
	4 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "PC-9821",
					'image'	: "btn_pc9821.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Mac IICi",
					'image'	: "btn_maciici.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Risc PC 700",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				4 : {
					'text'	: "SNES",
					'image'	: "btn_snes.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "HDMI KVM",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "VGA KVM",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				3 : {
					'text'	: "Speakers",
					'image'	: None,
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: ["speakers"],
				},
				4 : {
					'text'	: "Gamecube",
					'image'	: "btn_gamecube.bmp",
					'poweron'	: [],
					'poweroff'	: [],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
			},
		},
	},
}