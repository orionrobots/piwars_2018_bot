from piwars_bot import Robot

def main():
    with Robot() as robot:
      while True:
        print(robot.left_distance, robot.forward_distance, robot.right_distance)

if __name__ == "__main__":
  main()
