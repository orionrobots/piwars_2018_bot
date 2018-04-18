from contextlib import contextmanager
import piconzero as pz
from hcsr04 import getDistance as pz_getdistance

import RPi.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo,    GPIO.IN)

    def get_distance(self):
        # Send 10us pulse to trigger
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        start = time.time()
        count = time.time() 
        while GPIO.input(self.echo)==0 and time.time()-count<0.1:
            start = time.time()
        count=time.time()
        stop=count
        while GPIO.input(self.echo)==1 and time.time()-count<0.1:
            stop = time.time()
        # Calculate pulse length
        elapsed = stop-start
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000
        # That was the distance there and back so halve the value
        distance = distance / 2
        return distance

class _robot(object):
    def __init__(self):
        pz.init()
        # 24, 25 is BCM 18, 22
        self.sensor_left = DistanceSensor(echo=18, trigger=22)
        # 22, 23 is BCM 15, 16
        self.sensor_right = DistanceSensor(echo=15, trigger=16)

    @property
    def forward_distance(self):
        return pz.get_distance()

    @property
    def left_distance(self):
        return self.sensor_left.get_distance()

    @property
    def right_distance(self):
        return self.sensor_right.get_distance()

    def set_motors(self, left_speed, right_speed):
        pz.setMotor(0, max(min(int(left_speed), 100), -100))
        pz.setMotor(1, max(min(int(right_speed), 100), -100))

    def set_left(self, left_speed):
        pz.setMotor(0, max(min(int(left_speed), 100), -100))

    def set_right(self, right_speed):
        pz.setMotor(1, max(min(int(right_speed), 100), -100))

    def forward(self, speed):
        """Both motors forward"""
        pz.forward(speed)

    def left(self, speed):
        pz.spinLeft(speed)

    def right(self, speed):
        pz.spinRight(speed)

    def backward(self, speed):
        pz.forward(-speed)

    def stop(self):
        """Both motors stop"""
        pz.stop()

@contextmanager
def Robot():
    """Use this to ensure robot stops if inner code 
        crashes"""
    try:
        yield _robot()
    finally:
        pz.stop()
        pz.cleanup()
