"""Helper functions for timer and stopwatch."""
import random
import sys
import datetime
import os
import json
import math
from pathlib import Path


def genNNbsp(number):
    """Return string with &nbsp; repeated `number` times."""
    return "&nbsp;" * number


def padWithNbsp(s, length):
    """Add `&nbsp;` to the end of string to make `length` characters long."""
    return s.ljust(length, '^').replace('^', '&nbsp;')


def randomColorHex():
    """Generate random CSS color."""
    def r():
        return random.randint(0, 255)

    return f"#{r():0x}{r():0x}{r():0x}"


def countToText(count):
    """Convert int value into time to be shown in window"""
    tdShort = datetime.timedelta(seconds=math.floor(count / 10))
    tdFull = datetime.timedelta(seconds=count / 10)
    mStr = str(math.floor(tdFull.microseconds / 100000))
    return str(tdShort) + "." + mStr


def doSettingsExist(fileName):
    """Check if file with fileName exists in current directory."""
    return os.path.isfile(getCurrentDirectory() + "/" + fileName)


def writeSettingsFile(fileName, hashmap):
    """Write hashmap into JSON file with fileName."""
    with open(getCurrentDirectory() + "/" + fileName, 'w', encoding="utf-8") as f:
        f.write(json.dumps(hashmap))


def readSettingsFile(fileName):
    """Parse JSON file with fileName into a hashmap."""
    with open(getCurrentDirectory() + "/" + fileName, encoding="utf-8") as f:
        return json.load(f)


def readOrWriteSettings(fileName, defaultSettings=None):
    """
    Read settings from disk.

    If settings file doesn't exist, create it.
    If file exists and is not valid, exit.
    Return parsed settings.
    """
    if defaultSettings is None:
        defaultSettings = []
    if not doSettingsExist(fileName):
        print(fileName + " does not exist, creating it")
        writeSettingsFile(fileName, defaultSettings)

    settings = readSettingsFile(fileName)

    if not validateSettings(settings):
        print(fileName + " is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings


def getCurrentDirectory():
    """Get current directory (that contains python script)."""
    return os.path.dirname(os.path.realpath(__file__))


def validateSettings(settings):
    """Validate parsed settings."""
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

    return isinstance(settings, list)


def isAlreadyRunning(label="default"):
    """
    Detect if an an instance with the label is already running, globally at the operating system level.

    Using `os.open` ensures that the file pointer won't be closed
    by Python's garbage collector after the function's scope is exited.

    The lock will be released when the program exits, or could be
    released if the file pointer were closed.
    """
    if sys.platform == "win32":
        # Can't local file in windows
        return False

    import fcntl  # pylint: disable=import-outside-toplevel

    path = getCurrentDirectory() + "/" + label + '.lock'

    fle = Path(path)
    fle.touch(exist_ok=True)

    lockFilePointer = os.open(path, os.O_WRONLY)

    try:
        fcntl.lockf(lockFilePointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        alreadyRunning = False
    except IOError:
        alreadyRunning = True

    return alreadyRunning


def findFragmentSettingsIndex(settings, uid):
    """
    Find settings entry that corresponds to stopwatch/timer by uid.

    If it can't be found, create new settings entry.

    Return index of settings entry that was found or created.
    """
    fragmentSettingsArray = [i for i, x in enumerate(settings) if x["uid"] == uid]
    if len(fragmentSettingsArray) != 0:
        fragmentDictIndex = fragmentSettingsArray[0]
    else:
        fragmentDict = {"uid": uid}
        settings.append(fragmentDict)
        fragmentDictIndex = len(settings) - 1

    return fragmentDictIndex
