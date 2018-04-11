from contextlib import contextmanager
from gpiozero import DistanceSensor
import piconzero as pz

class _robot(object):
    def __init__(self):
        pz.init()
        self.sensor_mid = DistanceSensor(echo=20, trigger=20)

    @property
    def mid_distance(self):
        return self.sensor_mid.distance

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
