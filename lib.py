from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime
import os
import json
import fcntl
from pathlib import Path

SETTINGS_FILE = "multistopwatch.json"
DEFAULT_SETTINGS = []

def drawIcon(str="--", textColor = "#000", bgColor = "#fff"):
    pixmap = QPixmap(24, 24)
    pixmap.fill(QColor(bgColor))

    painter = QPainter(pixmap)
    painter.setPen(QColor(textColor))
    painter.setFont(QFont('Arial', 10))
    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str)
    painter.end()
    return QIcon(pixmap)

def genTextFull(count):
    tdShort = datetime.timedelta(seconds=round(count/10))
    tdFull = datetime.timedelta(seconds=count/10)
    mStr = str(round(tdFull.microseconds / 100000))
    return str(tdShort) + "." + mStr

def genTextShort(count):
    seconds = count / 10
    secondsInt = round(seconds)
    minInt = round(seconds / 60)
    hFloat = float(seconds) / 60 / 60
    hInt = round(seconds / 60 / 60)
    if seconds <= 99:
        return str(secondsInt) + "s"
    elif minInt < 60:
        return str(minInt) + "m"
    elif minInt >= 60 and hInt < 10:
        return str(round(hFloat, 1)) + "h"
    elif hInt >= 10:
        return str(hInt) + "h"

def doSettingsExist():
    return os.path.isfile(get_current_directory() + "/" + SETTINGS_FILE)

def writeSettingsFile(hashmap):
    with open(get_current_directory() + "/" + SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(hashmap))

def readSettingsFile():
    with open(get_current_directory() + "/" + SETTINGS_FILE) as f:
        return json.load(f)

def readWriteSettings():
    if not doSettingsExist():
        print("settings.json does not exist, creating it")
        writeSettingsFile(DEFAULT_SETTINGS)

    settings = readSettingsFile()

    if not validateSettings(settings):
        print("settings.json is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings

def get_current_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print("SCript path:", dir_path)
    return dir_path

def validateSettings(settings):

    # # for key in ["checkIsOut", "checkIsColliding"]:
    # #     if not(key in settings.keys()) or (type(settings[key]) != bool):
    # #         return False

    # # for key in ["cellNum", "intervalMilliseconds"]:
    # #     if not(key in settings.keys()) or (type(settings[key]) != int) or (settings[key] < 0):
    # #         return False

    # # if settings["cellNum"] < 2:
    # #     return False

    # key = "count"
    # if not(key in settings.keys()) or (type(settings[key]) != int) or (settings[key] < 0):
    #     return False

    # raise Exception(str(  isinstance(settings, list)    ))

    # return True

    return isinstance(settings, list)

def instance_already_running(label="default"):
    """
    Detect if an an instance with the label is already running, globally
    at the operating system level.

    Using `os.open` ensures that the file pointer won't be closed
    by Python's garbage collector after the function's scope is exited.

    The lock will be released when the program exits, or could be
    released if the file pointer were closed.
    """
    
    path = get_current_directory() + "/" + 'multistopwatch.lock'

    fle = Path(path)
    fle.touch(exist_ok=True)

    # lock_file_pointer = os.open(f"/tmp/instance_{label}.lock", os.O_WRONLY)
    lock_file_pointer = os.open(path, os.O_WRONLY)

    try:
        fcntl.lockf(lock_file_pointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        already_running = False
    except IOError:
        already_running = True

    return already_running