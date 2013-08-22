#!/usr/bin/env python
# -*- coding: utf-8 -*-


HOST = "localhost"
PORT = 4223
UID = "6jDX7j" # Change to your UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_stepper import Stepper

import argparse
from time import sleep


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test Stepper Motor!')
    parser.add_argument('device', metavar='N', type=str, nargs='+', help='a device name e.g. stepper or lcd')
    parser.add_argument('id', metavar='M', type=str, nargs='+', help='id of device')
    parser.add_argument('steps', metavar='steps', type=int, nargs='+', default=50, help='integer')

    args = parser.parse_args()

    ipcon = IPConnection() # Create IP connection
    stepper = Stepper(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

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
    print stepper.get_current_consumption()
    sleep(3)
    stepper.disable()

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()
