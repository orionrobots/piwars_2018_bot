"""Wall avoiding"""
from piwars_bot import Robot
from piwars_bot_controller import PiWarsController

forward_speed = 100
reverse_speed  = -35
forward_react_dist = 18
hyst_react_dist = 20

def main():
    mode = 'Waiting for first reading'
    with Robot() as robot: #, PiWarsController().connect_pad() as joystick:
        while True: #joystick.connected and not joystick['home']:
            # of left, right and forward - which is furthest?
            left = robot.left_distance
            forward = robot.forward_distance
            right = robot.right_distance
            print(left, forward, right, mode)
            if mode == 'turning left' and (
	        	forward < hyst_react_dist or
	                right < hyst_react_dist):
                robot.set_left(reverse_speed)
            elif mode == 'turning right' and (
                  forward < hyst_react_dist or
                  left < hyst_react_dist):
                robot.set_right(reverse_speed)
            elif forward > forward_react_dist:
                robot.set_left(forward_speed)
                robot.set_right(forward_speed)
                mode = 'forward'
            else:
                if left < right:
                    mode = 'turning right'
                    robot.set_right(reverse_speed)
                else:
                    mode = 'turning left'
                    robot.set_left(reverse_speed)

if __name__ == '__main__':
    main()
