# sdlRFController
SDL touchscreen interface for Raspberry Pi - using RF transmitter to control home power sockets.

![Example image](docs/example.jpg  "Example image")

It can process sequences of actions to automate turning on or off multiple devices at the same time. For example:

 - First turn on the TV
 - Then turn on the speakers
 - Then turn on your upscaler box
 - Finally turn on the Sega Megadrive

All mapped to a single button on the touchscreen.

---

## Requirements

**Hardware requirements:**

 - Raspberry Pi (tested on 2b and 3b)
 - [Waveshare 3.5" touchscreen](https://www.waveshare.com/3.5inch-rpi-lcd-a.htm) 
 - [RFM69 Radio Module](https://www.google.com/search?q=rfm69+radio&oq=rfm69+radio) or the [Energenie 314-RT](https://energenie4u.co.uk/catalogue/product/ENER314-RT) 
 - One or more [Energenie RF controlled power sockets](https://energenie4u.co.uk/) (tested with ENER02 and ENER010)
 
 **Software requirements**
 
  - Python 3
  - PySDL2 - which requires the following libraries:
    - libSDL2
    - libSDL2-TTF
  
A `requirements.txt` file is provided with which you can automatically install all of the Python packages, simply run:

```
pip install -r requirements.txt
```

### libSDL without X11 for Raspbian

Earlier versions of libSDL2 for Raspbian required the installation of the X11 server in order to produce graphics output. Clearly doing that is running extra stuff that we really don't want or need.

From libSDL2 v2.0.5 output using OpenGL ES *without* X11 running should be supported. You can force SDL to use this mode by setting the following environment variable before running your application:

```
export SDL_RENDER_DRIVER=opengles2
```

Make sure you have the latest version of Raspbian installed. If you want to have the absolute latest version of libSDL2 which has the non-X11 OpenGL ES support, the SDL project provides pre-built packages here: https://buildbot.libsdl.org/sdl-builds/sdl-raspberrypi/?C=M;O=D

Test the application first, it's likely that you already have a version of libSDL2 with the non-X11 OpenGL ES support.

### Installing energenie library

The Python library to talk to the Energenie RF controlled power sockets is maintained here: https://github.com/whaleygeek/pyenergenie

sdlRFController doesn't need the full package installing, just the C driver and the Energenie device library. You can find them here:

 - [Energenie C device driver](https://github.com/whaleygeek/pyenergenie/tree/master/src/energenie/drv) 
 - [Energenie Python library](https://github.com/whaleygeek/pyenergenie/tree/master/src/energenie) 
 
Presuming you have a directory called *sdlRFController* with my code checked out already, you'll then need to do the following:

```
cd sdlRFController
mkdir tmp
cd tmp
git clone https://github.com/whaleygeek/pyenergenie
cd ..
mv tmp/pyenergenie/energenie .
rm -rf tmp
```

Of course, you are free to place the `pyenergenie` directory anywhere you want and just symlink it in, if you wish.

That will leave you with just the `energenie` sub directory of the pyenergenie project. You then have to compile the C driver:

```
cd energenie/drv
sh build_rpi
```

The resulting binary doesn't need to be installed, the pyenergenie code (and, ultimately sdlRFController) will use it from where you built it.

### Installing touchscreen

TO DO

### Installing Radio module

#### RFM69 module 
 
 see: https://rpi-rfm69.readthedocs.io/en/latest/hookup.html
 
 ![RFM69 Wiring](docs/rfm69_wires.jpg  "RFM69 Wiring")
 
#### Energenie 314-RT module
 
 See: https://energenie4u.co.uk/res/pdfs/ENER314-RT%20User%20Guide%20V2.pdf

![ENER314-RT Wiring](docs/ener314rt_wires.jpg  "ENER314-RT Wiring")

Be aware that if using the Waveshare 3.5" touchscreen that some of the pins needed for the SPI interface of the radio modules are either obscured or in use by the screen. If this is the case you will need to change (at least) the chip-enable (*CE*) pin that the radio module uses; shared used of MISO, MOSI, SCLK, Vin, Gnd *should* all be okay.

---

## Configuring devices

Every device that you want to control must have an entry in the file `libs/config.py`.

The configuration of a device is fairly simple. Each device is represented by a single button on the screen, a button has the following elements defined as a Python dictionary:

| Key | Value |
|------|---------|
| text | Name of the device or activity the power switch refers to |
| image | A bitmap which is shown as the picture for this button *(Note: Image must be no larger than 200x60)*|
| poweron | A series of actions that are taken when pressing this button to turn on the device or activity. |
| poweroff | A series of actions that are taken when pressing this button to turn on the device or activity |
| remote | The home code / remote code / device id that the power strip or switch is keyed to that this device is plugged in to |
| socket | For multi-socket power strips *(ENER010)*, the physical socket that this device is plugged in to |
| tags | metadata which categorises this device. For example: "downstairs lights", "speaker system", "consoles in the boys room", "computer", etc. |

An example button/device for my Roland MT-32 MIDI synthesiser could be:

```
'text'	: "MT-32",
'image'	: "btn_mt32.bmp",
'poweron' : [
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "ON"},	# Turn this remote socket on
],
'poweroff' : [
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
],
'remote'	: 0xABCD,
'socket'	: 1,
'tags'	: ["midi"],
```

A little bit of explanation is needed for the above.

 - `btn_mt32.bmp` this image is a 200x600 bitmap stored in the `assets` directory.
 
 - If the *image* field was set to *None*, instead of the bitmap, it would print the *text* field on the button instead - useful when you don't have/need a graphical button, but a simple label will do instead.
 
 - `poweron` - when pressing the on button, we are going to send a single power signal, *"ON"*, using the remote code *0xABCD*, to socket *1*. This corresponds to the single socket we paired the device to. 
    - Syntax 1: `{ 'remote' : REMOTE_ID, 'socket' : SOCKET_NUMBER, 'action' : ["ON"|"OFF"]}`
    
    - Syntax 2: `{ 'tags' : ["tag1", "tag2", "tagN"], 'action' : ["ON"|"OFF"]}`

 - `poweroff` - The same syntax options as `poweron`.

- `tags` - we're tagging this device as *midi*, as we have multiple of these devices that we may want to manage all-together, at some future point.

You should already be able to see that having multiple actions listed for both the `poweron` and `poweroff` variables means that we can automate several series of events. 

### Remote Control Codes

Unfortunately, Energenie remote controls do not have their unique device id / house number / remote id printed on them. The sticker you usually find is either a batch or production code.

When you pair a remote to a power strip/switch, then power switch learns the unique id of the remote you are broadcasting and then only responds to messages broadcast with that id.

Sadly, it's still a bit tricky to work out the device id of a remote. 

For a workaround, see https://github.com/whaleygeek/pyenergenie/issues/81#issuecomment-273619134

Specifically, you need a USB stick supported by RTL-SDR (like a Realtek RTL2832 based DVB), run the RTL-SDR software (https://github.com/merbanan/rtl_433) and monitor the output whilst you pair a Energenie remote control with a power socket. That *should* capture the unique id of your remote control.

You should see output as follows when running `rtl_433 -a`:

```
[00] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[01] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[02] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[03] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[04] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[05] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
[06] {25} 8b 4e 87 00 : 10001011 01001110 10000111 0
```

The first 6 hexadecimal characters of the capture output (e.g. 8b 4e 87 in the sample above) should be the id of the remote.

### Macros / Complex Events

Since both the `poweron` and `poweroff` events are list items and can take more than one element, we are free to add multiple actions.

Going back to the example of our Roland MIDI synth, it might make sense when turning on the MIDI module to also turn on the speakers/amplifier and power up the stereo mixer deck. Presuming each of those other devices also have configuration entries (let us say they are represented by another remote id 0xDCBA, using sockets 2 and 3), we could write that `poweron` action as follows:

```
'text'	: "MT-32",
'image'	: "btn_mt32.bmp",
'poweron' : [
		{'remote' : 0xDCBA, 'socket' : 2, 'action' : "ON"},	# Turn on speakers
		{'remote' : 0xDCBA, 'socket' : 3, 'action' : "ON"},	# Turn on stereo mixer
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "ON"},	# Turn the MT-32 MIDI module on
],
'poweroff' : [
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
],
'remote'	: 0xABCD,
'socket'	: 1,
'tags'	: ["midi"],
```

Since (in this case) we're dealing with MIDI/music playback, we may also want to turn on a MIDI keyboard or something else as well as speakers, amplifier and mixer. We could continue adding multiple entries in to the `poweron` list, but instead it may be easier to aggregate those items in to a common set of devices. 
For this purpose, we can use the `tags` field.

Presuming our amplifier, mixer deck, speakers and other audio output equipment each has a config entry with the correct remote id and socket, and each of them also has the `tags` entry *"speaker system"* we could instead write:

```
'text'	: "MT-32",
'image'	: "btn_mt32.bmp",
'poweron' : [
		{'tags' : ["speaker system"], 'action' : "ON"},		# Turn on any device with a tag of 'speakers'
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "ON"},	# Turn the MT-32 MIDI module on
],
'poweroff' : [
		{'remote' : 0xABCD, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
],
'remote'	: 0xABCD,
'socket'	: 1,
'tags'	: ["midi"],
```

That would generate a list of individual `poweron` events for any device tagged as *"speaker system", and then finally send a power on signal to the MIDI device.

As the Energenie remote sends discrete *ON* or *OFF* codes, it is safe to send the *ON* code to a device that is already powered on, so we don't need to *(and in fact the system is one-way signalling so we cannot)* check the power status of a device before we send the signal.

## Placing Buttons on Screen

The arrangement of buttons on the screen interface is achieved through *pages*, *columns* and *rows*.

Every *page* on the device (numbered from **1** upwards) is split in to two columns; **left** (referred to as *"L"*) and **right** (referred to as *"R"*).

There are (up to) 4 rows of buttons (each button in a column is numbered from **1** to **4**).

The layout is managed through the `libs/config.py` file, via the variable `SCREENS`.

Here is a sample layout for 1 page, 2 columns (3 buttons on the left, 1 on the right):

```
SCREENS = {
	# First page
	1 : {
		'BUTTON' : { 
			'L' : {
				1 : {
					'text'	: "Monitor",
					'image'	: None,
					'poweron' : [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "ON"},	# Turn this remote socket off
					],
					'poweroff' : [
						{'remote' : 0x0000, 'socket' : 1, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0x0000,
					'socket'	: 1,
					'tags'	: [],
				},
				2 : {
					'text'	: "Amplifier",
					'image'	: None,
					'poweron' : [
						{'remote' : 0x0000, 'socket' : 2, 'action' : "ON"},	# Turn this remote socket off
					],
					'poweroff' : [
						{'remote' : 0x0000, 'socket' : 2, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0x0000,
					'socket'	: 2,
					'tags'	: [],
				},
				3 : {
					'text'	: "Upscaler",
					'image'	: None,
					'poweron' : [
						{'remote' : 0x0000, 'socket' : 3, 'action' : "ON"},	# Turn this remote socket off
					],
					'poweroff' : [
						{'remote' : 0x0000, 'socket' : 3, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0x0000,
					'socket'	: 3,
					'tags'	: [],
				},
			},
			'R' : {
				1 : {
					'text'	: "Sega Megadrive",
					'image'	: None,
					'poweron' : [
						{'remote' : 0x0000, 'socket' : 4, 'action' : "ON"},	# Turn this remote socket off
					],
					'poweroff' : [
						{'remote' : 0x0000, 'socket' : 4, 'action' : "OFF"},	# Turn this remote socket off
					],
					'remote'	: 0x0000,
					'socket'	: 4,
					'tags'	: [],
				},
			},
		},
	},
	# 2: {} # Page 2 doesn't exist in this layout
}
```

You are free to layout buttons on pages as you see fit. In my own use case I'm putting all the video games together on one page, display equipment on another, sound and music on another, etc.