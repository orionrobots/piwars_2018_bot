"""PiWars Robot WS2801 Menu System"""
from time import sleep
import subprocess
from piwars_bot_display import RobotDisplay
from piwars_bot_controller import PiWarsController

modes = [
    {'name': 'drive', 'process': 'dualshock_tank.py'},
    {'name': 'skittle track', 'process': 'skittle_track.py'}, 
    {'name': 'over the rainbow', 'process': 'over the rainbow`.py'}, 
    {'name': 'straight line speed', 'process': 'straight_speed.py'},
    {'name': 'maze', 'process': 'maze.py'},
    {'name': 'shutdown', 'process': 'shutdown_robot.py'}
]

class PiWarsModeMenu:
    def __init__(self):
        # Setup, but don't connect joypad devices
        self.menu = modes
        self.current_item = 0
        self.display = RobotDisplay()
        
    def action_menu_item(self):
        item = modes[self.current_item]
        self.display.message_menu_item_activated()
        subprocess.call(['python', item['process']])
        if item['name'] is 'shutdown':
            exit(0)

    def mainloop(self):
        while True:
            #   connect to joypad devices or show error
            controller = PiWarsController()
            action = False
            try:
                with controller.connect_pad() as pad:
                    self.display.message_menu_mode()
                    while pad.connected and not action:
                        sleep(0.05) # 50 millis
                        self.display.update()
                        #   allow mode selection with the dpad
                        presses = pad.check_presses()
                        if presses['dleft'] and self.current_item < len(modes):
                            self.current_item += 1
                            self.display.message_menu_set_current_item(self.current_item, modes[self.current_item]['name'])
                        if presses['dright'] and self.current_item > 0:
                            self.current_item -= 1
                            self.display.message_menu_set_current_item(self.current_item, modes[self.current_item]['name'])
                        if presses['cross']:
                            action = True
                if action:
                    #   then X button will deinitialise (cleanup) and start the subprocess
                    self.action_menu_item()
            finally:
                # display pad not connected
                self.display.message_waiting_for_pad()

def main():
    menu = PiWarsModeMenu()
    menu.mainloop()

if __name__ == '__main__':
    main()