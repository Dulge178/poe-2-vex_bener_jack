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

def driveStraightData(e):
  """
  1. Report position, rotation, and error
  2. Parameter: 3 = error value (setpoint - rotation)
  """
  brain.screen.set_cursor(1,1)
  brain.screen.print("Position: " + str(leftMotor.position())) # returns position

  brain.screen.set_cursor(2,1)
  brain.screen.print("Rotation: " + str(inertial_1.rotation())) # returns rotation

  brain.screen.set_cursor(3,1)
  brain.screen.print("Error: " + str(e)) # error value (setpoint - rotation)

def stopMotors():
  rightMotor.stop()
  leftMotor.stop()
  wait(0.5, SECONDS)

def driveStraight(distance, setpoint, motorVelocity):
  """
  1. distanc = distance in inches
  2. setpoint = 0-deg for driving straight
  3. motorVelocity = nominal velocity (+) => Forward, (-) => Backward
  """

  inertial_1.reset_rotation() #Reset the rotation value before moving

  kP = 0.25 # Proportional constant for driving straight
            # Used to calibrate the velocity correction term
            # if too small the correction will occur too slowly
            # if too large the system will over correct
            # determine the best by iteratively testing 
  
  # Calculate the distance in terms of encoder count
  wheelDiameter = 4 # Units = inches
  wheelCircumfrence = wheelDiameter * math.pi # Units = inches

  #distance(ticks) = (distance(inches) / Wheel Circumfrence) * 100
  distance = (distance/wheelCircumfrence) * 360 # units = ticks


  # Reset the motor encoders
  leftMotor.set_position(0, DEGREES)
  rightMotor.set_position(0, DEGREES)


  # Drive straight forward if motor velocity > 0
  if(motorVelocity > 0):
    # Use a while loop track the distance traveled
    while(leftMotor.position() < distance):
      error = (setpoint - inertial_1.rotation()) # Rotation error
      correction = kP * error # Motor velocity correction term

      # Correct the motor velocities to maintain course
      # If error > 0 => drift left
      # If error < 0 => drift right


      leftMotor.set_velocity((motorVelocity + correction), PERCENT)
      rightMotor.set_velocity((motorVelocity - correction), PERCENT)

      #Spin the motors
      leftMotor.spin(FORWARD)
      rightMotor.spin(FORWARD)
    
      driveStraightData(error) # Display current position, rotation, & error

    stopMotors() # Stop both motors when the desired distance is traveled
                 # You will need to account for momentum

  else: 
    distance *= -1 # Distance count must be negative for driving reverse
    # Use a while loop track the distance traveled
    while(leftMotor.position() > distance):
      error = (setpoint - inertial_1.rotation())  # Rotation Error
      correction = kP * error # Motor velocity correction terms

      # Correct the motor velocities to maintain course
      # If error > 0 => drift left
      # If error < 0 => drift right

      leftMotor.set_velocity((motorVelocity + correction), PERCENT)
      rightMotor.set_velocity((motorVelocity - correction), PERCENT)

      #Spin the motors
      leftMotor.spin(REVERSE)
      rightMotor.spin(REVERSE)

      driveStraightData(error) # Display current position, rotation & error

    stopMotors() # Stop both motors when the desired distance is traveled
                 # You will need to account for momentum



    #--------------------define main function-----------------------------#
def main():
  """
  This is the function that will be executed by the brain
  """

  bump()     #Call bump function to begin the program
  #set stopping value  for left and right motors
  leftMotor.set_stopping(COAST)
  rightMotor.set_stopping(COAST)
  intertialCalibration()   #calibrate the inertial sensor
  testInertial()   #test the inertial heading and rotation

  driveStraight(90, 0, 50) # TUne your KP Value
  
main()
