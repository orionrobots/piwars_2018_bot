# Picon Zero Dualshock tank drive
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct
from piwars_bot_controller import PiWarsController
from piwars_bot import Robot

print("Tests the motors by using the dualshock pad")

pz.init()
try:
    print("Controller setup")
    with PiWarsController().connect_pad() as joystick, Robot() as robot:
        while joystick.connected and not joystick['home']:
            left_track = int(joystick.ly * 100)
            right_track = int(joystick.ry * 100)
            robot.set_left(left_track)
            robot.set_right(right_track)
            if left_track != 0 or right_track != 0:
              print("l {0:02} r {1:02}".format(left_track, right_track))

    print("Controller disconnected")
