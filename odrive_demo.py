#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
from walking import walking
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# Calibrate motor and wait for it to finish
print("starting calibration...")
my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

while my_drive.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)


while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(0.1)


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
print("Position setpoint is " + str(my_drive.axis0.controller.pos_setpoint))

# And this is how function calls are done:
for i in [1,2,3,4]:
    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))



my_drive.axis0.motor.config.current_lim = 75
my_drive.axis0.controller.config.vel_limit = 64000
time.sleep(0.1)

my_drive.axis1.motor.config.current_lim = 75
my_drive.axis1.controller.config.vel_limit = 64000
time.sleep(0.1)

# Testing speed settings 
# my_drive.axis0.controller.vel_setpoint = 3000 * 2*3.14/60 

# A sine wave to test
t0 = time.monotonic()
while True:
    my_drive.axis0.controller.config.vel_limit = 16000
    my_drive.axis1.controller.config.vel_limit = 16000
    time.sleep(0.1)


    print("New Velocity: 16000")
    for i in range(4):
      my_drive.axis0.controller.pos_setpoint = 8000
      my_drive.axis1.controller.pos_setpoint = 8000
      print("8000")
      time.sleep(.25)
    for x in range(4):
      print("0")
      my_drive.axis0.controller.pos_setpoint = 0
      my_drive.axis1.controller.pos_setpoint = 0
      time.sleep(.25)


# Some more things you can try:

# Write to a read-only property:
my_drive.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`

# Assign an incompatible value:
my_drive.motor0.pos_setpoint = "I like trains"  # fails with `ValueError: could not convert string to float`
