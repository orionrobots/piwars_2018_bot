# Picon Zero Dualshock tank drive
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct

import piconzero as pz, time

from approxeng.input.dualshock3 import DualShock3
from approxeng.input.controllers import find_single_controller
from approxeng.input.selectbinder import ControllerResource

def setup_controller():
    devices, controller, p = find_single_controller(controller_class = DualShock3)
    devices = [devices[0]]
    return devices, controller, p
    
print("Tests the motors by using the dualshock pad")

pz.init()
try:
    devices, controller, p = setup_controller()
    with ControllerResource(devices=devices, controller=controller) as joystick:
        while joystick.connected:
            left_track = joystick.ly
            right_track = joystick.ry
            pz.setMotor(0, left_track * 100)
            pz.setMotor(0, right_track * 100)

finally:
    pz.cleanup()
