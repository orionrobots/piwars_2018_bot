"""Interface to the chosen controller and manage it"""
from contextlib import contextmanager
from approxeng.input.dualshock3 import DualShock3
from approxeng.input.controllers import find_single_controller
from approxeng.input.selectbinder import ControllerResource

def setup_controller():
    devices, controller, p = find_single_controller(controller_class = DualShock3)
    devices = [devices[0]]
    return devices, controller, p

class PiWarsController:
    @contextmanager
    def connect_pad(self):
        """Connect the controller and yield it"""
        try:
            devices, controller, p = setup_controller()
            cr = ControllerResource(devices=devices, controller=controller)
        except:
            yield None
            return
        with cr as joystick:
            yield joystick
