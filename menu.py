"""PiWars Robot WS2801 Menu System"""

modes = {
    1: {'name': 'drive', 'process': 'dualshock_tank.py'},
    2: {'name': 'skittle track', 'process': 'skittle_track.py'},
    3: {'name': 'over the rainbow', 'process': 'over the rainbow.py'},
    4: {'name': 'straight line speed', 'process': 'straight_speed.py'},
    5: {'name': 'maze', 'process': 'maze.py'},
    6: {'name': 'shutdown', 'process': 'shutdown_robot.py'}
}

class PiWarsModeMenu:
    def __init__(pass):
        # Setup, but don't connect joypad devices

    def mainloop(self):
        while True:
            #   connect to joypad devices or show error
            #   display a menu mode (blinking mode 1 light)
            #   allow mode selection with the dpad
            #   then X button will deinitialise (cleanup) and start the subprocess

def main():
    menu = PiWarsModeMenu()
    menu.mainloop()

if __name__ == '__main__':
    main()