import logging
import coloredlogs
import time
coloredlogs.install()
def error(msg:str):
    logging.error(msg)

def warning(msg:str):
    logging.warning(msg)

def info(msg:str):
    logging.info(msg)

def debug(msg:str):
    logging.debug(msg)

if __name__ == '__main__':
    info("hello world")