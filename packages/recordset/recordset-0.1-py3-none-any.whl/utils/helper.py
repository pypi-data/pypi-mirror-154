import logging
import os
import subprocess
import sys

from utils import logger

LOGGING_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO
}
# # ECS CLI  contants

MAC_OS = 'mac'
LINUX_OS = 'linux'


def cmd_exec(str):
    logger.debug("\n------------------------ Executing Command: Start ------------------------")
    logger.debug("\n$>>" + str)
    output = os.popen(str).read().strip()
    logger.debug("\n$>>" + output)
    logger.debug("\n------------------------ Executing Command: END ------------------------")
    return output


def join_me(stringList):
    return "".join(string for string in stringList)


def running_cmd(cmd):
    logger.log_c("Running command: ", cmd)
    subprocess.call(cmd.split(" "))


def get_system_type():
    platform = sys.platform;
    logger.debug("Platform : " + platform)
    system_name = "NA";
    if platform == "linux" or platform == "linux2":
        system_name = LINUX_OS
    elif platform == "darwin":
        system_name = MAC_OS

    logger.debug("System Name : " + system_name)
    return system_name;


def helper():
    print('\n------------------------ Command Options ------------------------')
    print('\nrecordset is a simple demo')
    print('\n')
