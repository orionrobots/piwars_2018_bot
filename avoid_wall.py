"""Wall avoiding"""
from piwars_bot import Robot
from piwars_bot_controller import PiWarsController

def main():
    with Robot() as robot, PiWarsController().connect_pad() as joystick:
        while joystick.connected and not joystick['home']:
            # of left, right and forward - which is furthest?
            left = robot.left_distance
            forward = robot.forward_distance
            right = robot.right_distance
            if forward > left:
                robot.set_left(100)
            else:
                robot.set_left(0)
            if forward > right:
                robot.set_right(100)
            else:
                robot.set_right(0)


if __name__ == '__main__':
    main()