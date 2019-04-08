# Instruction on Wiring

# LED Light Strip WS2812B to GPIO:

DI ---> Pin 12 (GPIO 18)

5V ---> Pin 2 (or any 5V)

GND ---> Pin 14 (or any GND)

![Screenshot](images/wiring1.jpg)


# RFID RC522 Chip to GPIO:

SDA connects to Pin 24.

SCK connects to Pin 23.

MOSI connects to Pin 19.

MISO connects to Pin 21.

GND connects to Pin 6.

RST connects to Pin 22.

3.3v connects to Pin 1.

# Audio not playing on USB Speaker:

Open sudo nano /usr/share/alsa/alsa.conf and look for the following two lines:
```
defaults.ctl.card 0
defaults.pcm.card 0
```
Change both “0” to “1” and then save the file.
```
defaults.ctl.card 1
defaults.pcm.card 1
```
# References:

How to setup a Raspberry Pi RFID RC522 Chip:

https://pimylifeup.com/raspberry-pi-rfid-rc522/

Connect and Control WS2812 RGB LED Strips via Raspberry Pi:

https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/