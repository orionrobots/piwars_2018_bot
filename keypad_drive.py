# Picon Zero Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct

import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 60

print("Tests the motors by using the arrow keys to control")
print("Use , or < to slow down")
print("Use . or > to speed up")
print("Left track - 1 back,4 stop,7 for")
print("Right track - 3 back,6 stop ,9 for")
print("Space to stop")
print("Speed changes take effect when the next arrow key is pressed")
print("Press Ctrl-C to end")
print()

pz.init()

# main loop
try:
    while True:
        keyp = readkey()
        if keyp == "1":
            pz.setMotor(0, -speed)
            print("Motor 0 back", speed)
        elif keyp == "4":
            pz.setMotor(0, 0)
            print("Motor 0 stop")
        elif keyp == "7":
            pz.setMotor(0, speed)
            print("Motor 0 forward", speed)
        elif keyp == "3":
            pz.setMotor(1, -speed)
            print("Motor 1 back", speed)
        elif keyp == "6":
            pz.setMotor(1, 0)
            print("Motor 1 stop")
        elif keyp == "9":
            pz.setMotor(1, speed)
            print("Motor 1 forward", speed)
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+10)
            print('Speed+', speed)
        elif keyp == ',' or keyp == '<':
            speed = max (0, speed-10)
            print('Speed-', speed)
        elif keyp == ' ':
            pz.stop()
            print('Stop')
        elif ord(keyp) == 3:
            break

except KeyboardInterrupt:
    print()

finally:
    pz.cleanup()
    
