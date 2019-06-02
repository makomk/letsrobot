import os
import tempfile
import uuid
import logging

log = logging.getLogger('LR.tts.flite')

tempDir = None
hw_num = None
voice = None

def setup(robot_config):
    global tempDir
    global hw_num
    global voice

    voice = robot_config.get("flite", "voice")
    
    if robot_config.has_option('tts', 'speaker_num'):
        hw_num = robot_config.get('tts', 'speaker_num')
    else:
        hw_num = robot_config.get('tts', 'hw_num')
    
    #set the location to write the temp file to
    tempDir = tempfile.gettempdir()
    log.info("TTS temporary directory : %s", tempDir)

def say(*args):
    message = args[0]

    tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
    f = open(tempFilePath, "w")
    f.write(message)
    f.close()

    os.system('flite -voice ' + voice + ' -f ' + tempFilePath  + ' ' + tempFilePath + '.wav ')
    os.system('aplay -D plughw:{} '.format(hw_num) + tempFilePath + '.wav')
    os.remove(tempFilePath + '.wav')
    os.remove(tempFilePath)
    
