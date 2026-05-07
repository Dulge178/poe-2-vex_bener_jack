# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Bener Dulger && Jack Pellegrini                                                        #
# 	Created:      5/7/2026, 9:03:12 AM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")
from vex import *

rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)


liftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
inertial_1 = Inertial(Ports.PORT5)
liftArmRotation = Rotation(Ports.PORT6, False)
bumpSwitch = Bumper(brain.three_wire_port.a)


def bump():
  """
  Hold the program's execution until the button is pressed.
  """
  #waiting for the bump switch to be pressed
  while(bumpSwitch.pressing() == False):
    wait(10, MSEC)

    brain.screen.set_cursor(1, 1)
    brain.screen.print("press the button to start the program")

    pass
  brain.screen.clear_line(1)
  brain.screen.set_cursor(1,1)
  brain.screen.print("Program executed")
  wait(1, SECONDS)
    

#--------------------define main function-----------------------------#
def main():
  """
  This is the function that will be executed by the brain
  """

  bump()     #Call bump function to begin the program

main()

