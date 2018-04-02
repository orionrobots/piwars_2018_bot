from approxeng.input.selectbinder import ControllerResource
from approxeng.input.dualshock3 import DualShock3

while True:
    try:
        with ControllerResource() as joystick:
            print('Found a joystick and connected')
            while joystick.connected:
                # Do stuff with your joystick here!
                print("Lx {0:.2} ly {1:.2} rx {2:.2} ry {3:.2}".format(
			joystick.lx*1.0,
			joystick.ly*1.0,
			joystick.rx*1.0, 
			joystick.ry*1.0))
        # Joystick disconnected...
        print('Connection to joystick lost')
    except IOError:
        # No joystick found, wait for a bit before trying again
        print('Unable to find any joysticks')
        sleep(1.0)
