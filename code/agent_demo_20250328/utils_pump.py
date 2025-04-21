# utils_pump.py
# GPIO pin and suction pump related functions

print('Import suction pump control module')
import RPi.GPIO as GPIO
import time

# initialize GPIO
GPIO.setwarnings(False)   # do not print warning
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(20, 1)        # Turn off the suction pump solenoid valve

def pump_on():
    '''
    Turn on suction pump
    '''
    print('Turn on the suction pump')
    GPIO.output(20, 0)

def pump_off():
    '''
    Turn off the suction pump, vent the pump, and release the object
    '''
    print('Turn off the suction pump')
    GPIO.output(20, 1)   # Turn off the suction pump solenoid valve
    time.sleep(0.05)
    GPIO.output(21, 0)   # Open the vent valve
    time.sleep(0.2)
    GPIO.output(21, 1)
    time.sleep(0.05)
    GPIO.output(21, 0)   # Vent again to ensure the object is released
    time.sleep(0.2)
    GPIO.output(21, 1)
    time.sleep(0.05)