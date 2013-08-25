#!/usr/bin/env python
# -*- coding: utf-8 -*-


HOST = "localhost"
PORT = 4223
SUID = "6jDX7j" # UID from Stepper
LUID = "9ew" # UID from LCD

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_stepper import Stepper
from tinkerforge.bricklet_lcd_20x4 import LCD20x4

import argparse # parsing arguments for this script
from time import sleep # time delay
import sys # need for unicode
import types # need for unicode

# Callback LCD Button PRESSED
def cb_pressed(i):
    print('Pressed: ' + str(i))
    if str(i) == '2':
        if lcd.is_backlight_on():
            lcd.backlight_off() # Turn backlight on
        else:
            lcd.backlight_on() # Turn backlight on

# Callback LCD Button RELEASED
def cb_released(i):
    print('Released: ' + str(i))

# Maps a Python string to the LCD charset
def unicode_to_ks0066u(string):
    if sys.hexversion < 0x03000000:
        byte = lambda x: chr(x)
        ks0066u = ''

        if type(string) != types.UnicodeType:
            code_points = unicode(string, 'UTF-8')
        else:
            code_points = string
    else:
        byte = lambda x: bytes([x])
        ks0066u = bytes()
        code_points = string

    for code_point in code_points:
        code_point = ord(code_point)

        # ASCII subset from JIS X 0201
        if code_point >= 0x0020 and code_point <= 0x007e:
            # The LCD charset doesn't include '\' and '~', use similar characters instead
            mapping = {
                0x005c : byte(0xa4), # REVERSE SOLIDUS maps to IDEOGRAPHIC COMMA
                0x007e : byte(0x2d)  # TILDE maps to HYPHEN-MINUS
            }

            try:
                c = mapping[code_point]
            except KeyError:
                c = byte(code_point)
        # Katakana subset from JIS X 0201
        elif code_point >= 0xff61 and code_point <= 0xff9f:
            c = byte(code_point - 0xfec0)
        # Special characters
        else:
            mapping = {
                0x00a5 : byte(0x5c), # YEN SIGN
                0x2192 : byte(0x7e), # RIGHTWARDS ARROW
                0x2190 : byte(0x7f), # LEFTWARDS ARROW
                0x00b0 : byte(0xdf), # DEGREE SIGN maps to KATAKANA SEMI-VOICED SOUND MARK
                0x03b1 : byte(0xe0), # GREEK SMALL LETTER ALPHA
                0x00c4 : byte(0xe1), # LATIN CAPITAL LETTER A WITH DIAERESIS
                0x00e4 : byte(0xe1), # LATIN SMALL LETTER A WITH DIAERESIS
                0x00df : byte(0xe2), # LATIN SMALL LETTER SHARP S
                0x03b5 : byte(0xe3), # GREEK SMALL LETTER EPSILON
                0x00b5 : byte(0xe4), # MICRO SIGN
                0x03bc : byte(0xe4), # GREEK SMALL LETTER MU
                0x03c2 : byte(0xe5), # GREEK SMALL LETTER FINAL SIGMA
                0x03c1 : byte(0xe6), # GREEK SMALL LETTER RHO
                0x221a : byte(0xe8), # SQUARE ROOT
                0x00b9 : byte(0xe9), # SUPERSCRIPT ONE maps to SUPERSCRIPT (minus) ONE
                0x00a4 : byte(0xeb), # CURRENCY SIGN
                0x00a2 : byte(0xec), # CENT SIGN
                0x2c60 : byte(0xed), # LATIN CAPITAL LETTER L WITH DOUBLE BAR
                0x00f1 : byte(0xee), # LATIN SMALL LETTER N WITH TILDE
                0x00d6 : byte(0xef), # LATIN CAPITAL LETTER O WITH DIAERESIS
                0x00f6 : byte(0xef), # LATIN SMALL LETTER O WITH DIAERESIS
                0x03f4 : byte(0xf2), # GREEK CAPITAL THETA SYMBOL
                0x221e : byte(0xf3), # INFINITY
                0x03a9 : byte(0xf4), # GREEK CAPITAL LETTER OMEGA
                0x00dc : byte(0xf5), # LATIN CAPITAL LETTER U WITH DIAERESIS
                0x00fc : byte(0xf5), # LATIN SMALL LETTER U WITH DIAERESIS
                0x03a3 : byte(0xf6), # GREEK CAPITAL LETTER SIGMA
                0x03c0 : byte(0xf7), # GREEK SMALL LETTER PI
                0x0304 : byte(0xf8), # COMBINING MACRON
                0x00f7 : byte(0xfd), # DIVISION SIGN
                0x25a0 : byte(0xff)  # BLACK SQUARE
            }

            try:
                c = mapping[code_point]
            except KeyError:
                c = byte(0xff) # BLACK SQUARE

        # Special handling for 'x' followed by COMBINING MACRON
        if c == byte(0xf8):
            if len(ks0066u) == 0 or not ks0066u.endswith(byte(0x78)):
                c = byte(0xff) # BLACK SQUARE

            if len(ks0066u) > 0:
                ks0066u = ks0066u[:-1]

        ks0066u += c

    return ks0066u

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='stepperControll' ,description='Test Stepper Motor!')
    #parser.add_argument('device', metavar='N', type=str, nargs='+', help='a device name e.g. stepper or lcd')
    #parser.add_argument('idd', metavar='id', type=str, nargs='+', help='id of device')
    
    parser.add_argument('-s', action='store', dest='steps', type=int, default=50, help='Store a simple value')    
    #parser.add_argument('steps', metavar='steps', nargs='+',  help='integer')
    args = parser.parse_args()
    #print args.steps - yes is working! (test without devices..^^)

    ipcon =     IPConnection() # Create IP connection
    lcd =       LCD20x4(LUID, ipcon) # Create device object
    stepper =   Stepper(SUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # register callbacks from LCD Screen Button
    lcd.register_callback(lcd.CALLBACK_BUTTON_PRESSED, cb_pressed)
    lcd.register_callback(lcd.CALLBACK_BUTTON_RELEASED, cb_released)

    stepper.set_motor_current(800) # 800mA
    stepper.set_step_mode(8) # 1/8 step mode
    stepper.set_max_velocity(15) # Velocity 2000 steps/s

    # First Value:  Slow acceleration (500 steps/s^2), 
    # Second Value: Fast deacceleration (5000 steps/s^2)
    stepper.set_speed_ramping(50, 500) 

    print args

    print args.steps # 50 steps = 1mm
    step = int(args.steps[0])

    stepper.enable()
    stepper.set_steps(step) # Drive 60000 steps forward
    sleep(2)
    lcd.clear_display()
    # Write some strings using the unicode_to_ks0066u function to map to the LCD charset
    lcd.write_line(0, 0, unicode_to_ks0066u('Stepper Amp: ' + str(stepper.get_current_consumption()) + ' mA'))
    lcd.write_line(1, 0, unicode_to_ks0066u( str(args.idd) ))
    print stepper.get_current_consumption()
    sleep(10)
    stepper.disable()

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()
