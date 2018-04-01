from approxeng.input.selectbinder import ControllerResource

while True:
    try:
        with ControllerResource() as joystick:
            print('Found a joystick and connected')
            while joystick.connected:
                # Do stuff with your joystick here!
                print("Left track {0:.2}   Right track {1:.2}".format(joystick.ly, joystick.ry))
        # Joystick disconnected...
        print('Connection to joystick lost')
    except IOError:
        # No joystick found, wait for a bit before trying again
        print('Unable to find any joysticks')
        sleep(1.0)