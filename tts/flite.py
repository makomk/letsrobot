import os
import tempfile
import uuid
import logging
import subprocess
import re

log = logging.getLogger('LR.tts.flite')

tempDir = None
hw_num = None
voice = None
censor = None

ngr_re = re.compile(r" n i[hy] (?:g |jh )+(?:er|a[xa]?) ")
fg_re = re.compile(r" f ae g ")

def setup(robot_config):
    global tempDir
    global hw_num
    global voice
    global censor

    voice = robot_config.get("flite", "voice")
    censor = robot_config.getboolean('flite', 'censor')
    
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

    s = subprocess.check_output(['flite', '-ps', '-voice', voice, '-f', tempFilePath, tempFilePath+'.wav'])
    if censor and ngr_re.search(s):
        log.info("Censoring %r due to n-word (parsed as %r)", message, s.strip())
    elif censor and fg_re.search(s):
        log.info("Censoring %r due to that f-word (parsed as %r)", message, s.strip())
    else:
        os.system('aplay -D plughw:{} '.format(hw_num) + tempFilePath + '.wav')

    os.remove(tempFilePath + '.wav')
    os.remove(tempFilePath)
    
