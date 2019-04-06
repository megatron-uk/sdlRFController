APPLICATION_NAME = "sdlRFController"

# Enable more verbose output
DEBUG = 0
INFO = 1

# Screen size
SCREEN_W = 480
SCREEN_H = 320
SCREEN_BPP = 24

# Default screen fill
BACKGROUND_COLOUR = {
        'r'     : 0,
        'g'     : 0,
        'b'     : 0,
}
# Highlight colour
HIGHLIGHT_COLOUR = {
        'r'     : 200,
        'g'     : 200,
        'b'     : 200,
}

# Image folder
ASSETS_FOLDER = "./assets/"

# Flat graphics assets
ASSETS = {
        'splash' 		: ASSETS_FOLDER + 'splash.bmp', 
        'btn_default'	: ASSETS_FOLDER + 'btn_default.bmp',
        'btn_fwd'	: ASSETS_FOLDER + 'btn_default_fwd.bmp',
        'btn_back'	: ASSETS_FOLDER + 'btn_default_back.bmp',
}

# Font files
FONT_NORMAL = ASSETS_FOLDER + "verdana.ttf"
FONT_NORMAL_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_NORMAL_PT = 28

FONT_BUTTON = ASSETS_FOLDER + "verdanab.ttf"
FONT_BUTTON_COLOUR = { 'r' : 255, 'g': 255, 'b': 255}
FONT_BUTTON_PT = 28

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
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "SC-8820",
					'image'	: "btn_sc8820.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "SC-55",
					'image'	: "btn_sc55.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "Mixer",
					'image'	: None,
					'remote'	: 0x0000,
					'socket'	: 1,
				},
			},
			'R' : {
				1 : {
					'text'	: "Dreamcast",
					'image'	: "btn_dreamcast.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "Saturn",
					'image'	: "btn_saturn.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "Master System",
					'image'	: "btn_sms.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: "btn_megadrive.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
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
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "Playstation 2",
					'image'	: "btn_playstation2.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "Playstation 3",
					'image'	: "btn_playstation3.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "Playstation 4",
					'image'	: "btn_playstation4.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
			},
			'R' : {
				1 : {
					'text'	: "Vita",
					'image'	: "btn_playstationtv.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "XBox",
					'image'	: "btn_xbox.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "Xbox 360",
					'image'	: "btn_xbox360.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: None,
					'remote'	: 0x0000,
					'socket'	: 1,
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
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "Turbo Duo",
					'image'	: "btn_pcenginecd.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "Atari Jaguar",
					'image'	: "btn_atarijaguar.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "MSX",
					'image'	: "btn_msx.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
			},
			'R' : {
				1 : {
					'text'	: "Amiga 500",
					'image'	: "btn_amiga500.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				2 : {
					'text'	: "Amiga 1200",
					'image'	: "btn_amiga1200.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				3 : {
					'text'	: "Amstrad CPC",
					'image'	: "btn_amstradcpc.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
				4 : {
					'text'	: "Atari ST",
					'image'	: "btn_atarist.bmp",
					'remote'	: 0x0000,
					'socket'	: 1,
				},
			},
		},
	},
}