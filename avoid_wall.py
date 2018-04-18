"""Wall avoiding"""
from piwars_bot import Robot
from piwars_bot_controller import PiWarsController

def main():
    with Robot() as robot: #, PiWarsController().connect_pad() as joystick:
        while True: #joystick.connected and not joystick['home']:
            # of left, right and forward - which is furthest?
            left = robot.left_distance
            forward = robot.forward_distance
            right = robot.right_distance
            print(left, forward, right)
            robot.set_left(100)
            robot.set_right(100)
            if forward < left and forward < right:
                if left < right:
                    robot.set_left(0)
                else:
                    robot.set_right(0)
            elif forward < left:
                robot.set_right(0)
            elif forward < right:
                robot.set_left(0)


if __name__ == '__main__':
    main()
