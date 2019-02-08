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
sleepTime = None


def setup(robot_config):
    global TB
    global leftMotorMax
    global rightMotorMax
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
    sleepTime = robot_config.getfloat('diddyborg', 'sleep_time')


def move(args):
    global TB
    global leftMotorMax
    global rightMotorMax
    global sleepTime

    inverseRight = rightMotorMax * -1
    inverseLeft = leftMotorMax * -1

    direction = args['command']

    if direction == 'F':
        TB.SetMotor1(leftMotorMax)
        TB.SetMotor2(inverseRight)
        time.sleep(sleepTime)
        TB.SetMotor1(0.0)
        TB.SetMotor2(0.0)
    if direction == 'B':
        TB.SetMotor1(inverseLeft)
        TB.SetMotor2(rightMotorMax)
        time.sleep(sleepTime)
        TB.SetMotor1(0.0)
        TB.SetMotor2(0.0)
    if direction == 'L':
        TB.SetMotor1(leftMotorMax)
        TB.SetMotor2(rightMotorMax)
        time.sleep(sleepTime)
        TB.SetMotor1(0.0)
        TB.SetMotor2(0.0)
    if direction == 'R':
        TB.SetMotor1(leftMotorMax)
        TB.SetMotor2(rightMotorMax * -1)
        time.sleep(sleepTime)
        TB.SetMotor1(0.0)
        TB.SetMotor2(0.0)        
