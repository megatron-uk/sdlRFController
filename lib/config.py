APPLICATION_NAME = "sdlRFController"

# Enable more verbose output
DEBUG = 1
INFO = 1

# Screen size
SCREEN_W = 480
SCREEN_H = 320
SCREEN_BPP = 16

# Default screen fill
BACKGROUND_COLOUR = {
        'r'     : 0,
        'g'     : 0,
        'b'     : 0,
}

# Image folder
ASSETS_FOLDER = "./assets/"

# Flat graphics assets
ASSETS = {
        'splash' 		: ASSETS_FOLDER + 'splash.bmp', 
        'btn_default'	: ASSETS_FOLDER + 'btn_default.bmp'
}

# Screen layout and configuration
MAX_ROWS = 5
MAX_COLS = 2
# Reserved pixels between each row/button/top/bottom of screen
SCREEN_RESERVED_Y_PIXELS = 20
SCREEN_RESERVED_X_PIXELS = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
SCREENS = {
	# First page
	1 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "BLARGH",
					'image'	: "BLARGH.bmp",
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "WIBBLE",
					'image'	: "WIBBLE.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "SPLOO",
					'image'	: "SPLOO.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "PLOP",
					'image'	: "PLOP.bmp",
					'codes'	: ["111111", "1010101"],
				},
			},
			'R' : {
				1 : {
					'text'	: "BLARGH",
					'image'	: "BLARGH.bmp",
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "WIBBLE",
					'image'	: "WIBBLE.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "SPLOO",
					'image'	: "SPLOO.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "PLOP",
					'image'	: "PLOP.bmp",
					'codes'	: ["111111", "1010101"],
				},
			},
		},
	},
	# Second page
	# 2 : {}
}