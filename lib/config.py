APPLICATION_NAME = "sdlRFController"

# Enable more verbose output
DEBUG = 1
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

# Images used for button graphics should be this size
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

# A structure defining which buttons should be on which pages
SCREENS = {
	# First page
	1 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "MT-32",
					'image'	: "btn_mt32.bmp",
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "SC-8820",
					'image'	: "btn_sc8820.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "SC-55",
					'image'	: "btn_sc55.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "Mixer",
					'image'	: None,
					'codes'	: ["111111", "1010101"],
				},
			},
			'R' : {
				1 : {
					'text'	: "Dreamcast",
					'image'	: "btn_dreamcast.bmp",
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "Saturn",
					'image'	: "btn_saturn.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "Master System",
					'image'	: "btn_sms.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: "btn_megadrive.bmp",
					'codes'	: ["111111", "1010101"],
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
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "Playstation 2",
					'image'	: "btn_playstation2.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "Playstation 3",
					'image'	: "btn_playstation3.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "Playstation 4",
					'image'	: "btn_playstation4.bmp",
					'codes'	: ["111111", "1010101"],
				},
			},
			'R' : {
				1 : {
					'text'	: "Vita",
					'image'	: "btn_playstationtv.bmp",
					'codes'	: ["111111", "1010101"],
				},
				2 : {
					'text'	: "XBox",
					'image'	: "btn_xbox.bmp",
					'codes'	: ["111111", "1010101"],
				},
				3 : {
					'text'	: "Xbox 360",
					'image'	: "btn_xbox360.bmp",
					'codes'	: ["111111", "1010101"],
				},
				4 : {
					'text'	: "Megadrive",
					'image'	: None,
					'codes'	: ["111111", "1010101"],
				},
			},
		},
	},
}