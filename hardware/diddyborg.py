#pylint: disable=no-member
import ThunderBorg
import mod_utils
import logging
import time
import sys

log = logging.getLogger('LR.hardware.diddyBorg')

TB = ThunderBorg.ThunderBorg()
TB.Init()

leftMotorMax = None
rightMotorMax = None
#leftMotorTurnSpeed = None
#rightMotorTurnSpeed = None
#turnSleepTime = None
sleepTime = None


def setup(robot_config):
    global TB
    global leftMotorMax
    global rightMotorMax
#    global leftMotorTurnSpeed
#    global rightMotorTurnSpeed
#    global turnsSleepTime
    global sleepTime

    if not TB.foundChip:
        boards = ThunderBorg.ScanForThunderBorg()
        if len(boards) == 0:
            log.critical("No Thunderborg found. Check you are attached.")
        else:
            log.critical("No Thunderborg found at address %02X, Found boards at" % (TB.i2cAddress))
            for board in boards:
                log.critical('%02X (%d)' % (board, board))
            log.critical('Change the I2C Address so it is correct, e.g.')
            log.critical('TB.i2cAddress = 0x%02X' % (boards[0]))
        sys.exit(1)

    leftMotorMax = robot_config.getfloat('diddyborg', 'left_motor_max')
    rightMotorMax = robot_config.getfloat('diddyborg', 'right_motor_max')
#    leftMotorTurnSpeed = robot_config.getfloat('diddyborg', 'left_motor_turn_speed')
#    rightMotorTurnSpeed = robot_config.getfloat('diddyborg', 'right_motor_turn_speed')
#    turnSleepTime = robot_config.getfloat('diddyborg', 'turn_sleep_time')
    sleepTime = robot_config.getfloat('diddyborg', 'sleep_time')


def move(args):
    global TB
    global leftMotorMax
    global rightMotorMax
#    global leftMotorTurnSpeed
#    global rightMotorTurnSpeed
#    global turnSleepTime
    global sleepTime

    direction = args['command']

    inverseRight = rightMotorMax * -1
    inverseLeft = leftMotorMax * -1
#    inverseLeftTurn = leftMotorTurnSpeed * -1
#    inverseRightTurn = rightMotorTurnSpedd * -1

    if direction == 'F':
        TB.SetMotor1(inverseLeft)
        TB.SetMotor2(rightMotorMax)
    if direction == 'B':
        TB.SetMotor1(leftMotorMax)
        TB.SetMotor2(inverseRight)
    if direction == 'L':
        TB.SetMotor1(leftMotorMax)
        TB.SetMotor2(rightMotorMax)
    if direction == 'R':
        TB.SetMotor1(inverseLeft)
        TB.SetMotor2(inverseRight)
    if direction == 'stop':
        TB.SetMotor1(0.0)
        TB.SetMotor2(0.0)