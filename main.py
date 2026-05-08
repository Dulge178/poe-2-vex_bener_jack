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

brain.screen.print("This is where the brain prints to the screen")
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


def intertialCalibration():
  """
  1. Calibrate the intertial sensor
  2. A wait time of 2 seconds is required to calibrate the sensor
  3. The function is called at the start of the program execution
  """


  brain.screen.clear_screen()
  brain.screen.set_cursor(1,1)
  brain.screen.print("Calibrating the inertial sensor")
  brain.screen.set_cursor(2,1)
  brain.screen.print("Don't move the robot")
  inertial_1.calibrate()                    #calibrate the intertial sensor

  wait(2, SECONDS)                   #time required to calibrate the sensor          

  brain.screen.clear_screen()
  brain.screen.set_cursor(1,1)
  brain.screen.print("Calibration is complete!")

def testInertial():
  """
  1. Test the inertial sensor by having it diplay heading and rotation data.
  2. Press the button to end the test
  """

  brain.screen.clear_screen()
  while (bumpSwitch.pressing() == False):
    wait(10, MSEC)
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Heading: " + str(inertial_1.heading()))
    brain.screen.set_cursor(6, 1)
    brain.screen.print("Rotation: " + str(inertial_1.rotation()))
    brain.screen.set_cursor(8,1)
    brain.screen.print("Press the button to end the test")
  
  brain.screen.clear_screen()
  brain.screen.set_cursor(0,1)
  brain.screen.print("Inertial test is complete")

    #--------------------define main function-----------------------------#
def main():
  """
  This is the function that will be executed by the brain
  """

  bump()     #Call bump function to begin the program
  intertialCalibration()   #calibrate the inertial sensor
  testInertial()   #test the inertial heading and rotation

main()

