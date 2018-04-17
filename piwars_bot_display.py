import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import math

# Display notes
#  Lets just send messages to display - and let this class work out how to display them.
#  There are 3 kinds of message
#    Mode indication and selection - the menu system.
#    Debug - what the motors and sensors should be doing.
#    Error - any problems encountered.
#  In the console - this can translate to printing. The mode implementations may as well 
#  send values to this - they can then be used for mode display with a degree - as bars or colours.

class LedsPhysical:
    red = Adafruit_WS2801.RGB_to_color(255, 0, 0)
    green = Adafruit_WS2801.RGB_to_color(0, 255, 0)
    blue = Adafruit_WS2801.RGB_to_color(0, 0, 255)
    white = Adafruit_WS2801.RGB_to_color(255,255,255)
    yellow = Adafruit_WS2801.RGB_to_color(255, 255, 0)
    black = Adafruit_WS2801.RGB_to_color(0, 0, 0)

    def __init__(self):
        #      -------
        #      |* * *|     
        # -----------------
        # * * *|* * *|* * *
        # -----------------
        #
        #      |3 4 5|
        # -------------------
        # 0 1 2 6 7 8 9 10 11
        # -------------------
        self.count = 12
        self.front_panel = [LedsPhysical.black] * 6
        self.left_panel = [LedsPhysical.black] * 3
        self.right_panel = [LedsPhysical.black] * 3
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.count, spi=SPI.SpiDev(0, 0), gpio=GPIO)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        pass

    def display(self):
        nested_output = self.left_panel + self.front_panel  + self.right_panel
        for n, item in enumerate(nested_output):
            self.pixels.set_pixel(n, item)
        self.pixels.show()

    def set_front_panel(self, panel_list):
        if len(panel_list) == 6:
            self.front_panel = panel_list
        else:
            print("Warning - ignoring incorrect panel parameter %s" % panel_list)
        self.display()

    def set_front_panel_item(self, front_panel_position, colour):
        """Front panel:
        top row: 0 1 2
        next row: 3 4 5
        
        Colour is tuple r,g,b
        """
        self.front_panel[front_panel_position] = colour
        self.display()

    def set_left_panel(self, panel_list):
        if len(panel_list) == 3:
            self.left_panel = panel_list
        else:
            print("Warning - ignoring incorrect panel parameter %s" % panel_list)
        self.display()

    def set_right_panel(self, panel_list):
        if len(panel_list) == 3:
            self.right_panel = panel_list
        else:
            print("Warning - ignoring incorrect panel parameter %s" % panel_list)
        self.display()

    def clear_all(self):
        self.front_panel = [LedsPhysical.black] * 6
        self.left_panel = [LedsPhysical.black] * 3
        self.right_panel = [LedsPhysical.black] * 3
        self.display()


class RobotDisplay:
    def __init__(self):
        self.leds = LedsPhysical()
        self.mode = "start"
        self.anim_timer = 0
        self.menu_item = 0

    def update(self):
        """Call this every tick - so the display can animate itself"""
        self.anim_timer += 1
        if self.mode == 'menu' or self.mode == 'menu_activating':
            if self.anim_timer % 20 < 5:
                self.leds.set_front_panel_item(self.menu_item, LedsPhysical.blue)
            else:
                self.clear()
        if self.mode == 'menu_activating':
            frame = self.anim_timer % 20
            fader = math.sin((self.anim_timer % 360) /360) * 255
            colour = Adafruit_WS2801.RGB_to_color(0, fader, 0)
            self.leds.set_front_panel([colour] * 6)
        self.leds.display()

    def clear(self):
        self.leds.clear_all()

    def message_waiting_for_pad(self):
        print("Waiting for pad")
        self.leds.set_front_panel([LedsPhysical.red] * 6)
        self.leds.set_front_panel_item(0, LedsPhysical.yellow)

    def message_found_pad(self):
        pass

    def message_menu_mode(self):
        print("Entering menu mode")
        self.mode = 'menu'
        #   menu is front 6 items - first clear all
        self.clear()

    def message_menu_set_current_item(self, item_number, item_name):
        print("Current menu is {num}:{name}".format(num=item_number, name=item_name))
        self.menu_item = item_number

    def message_menu_item_activated(self):
        self.mode = 'menu_activating'
