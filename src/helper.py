import discord
import os # default module
from decouple import config
import inspect
import re
import coloredlogs
import verboselogs
import logging


def methodsWithDecorator(cls, decoratorName):
    sourcelines = inspect.getsourcelines(cls)[0]
    for i, line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@' + decoratorName:  # leaving a bit out
            c_line = sourcelines[i]
            nextLine = sourcelines[i + 1]
            function_name = nextLine.split('def')[1].split('(')[0].strip()
            name = re.search('(?<=name=")(.*?)(?=\")', c_line, flags=0).group(0)
            description = re.search('(?<=description=")(.*?)(?=\")', c_line, flags=0).group(0)
            print(name, description)
            yield(function_name)


def setup_logger(additional_info: str = None) -> verboselogs.VerboseLogger:
    logger = verboselogs.VerboseLogger("SimpsonBot")
    logger.addHandler(logging.StreamHandler())
    if additional_info:
        additional_info = f"[{additional_info}]"
    fmt = f"[%(asctime)s] [%(levelname)s] {additional_info or ''}{' ' if additional_info else ''}%(message)s"
    if config("LOG_LEVEL", 2, cast=int) == 0:
        coloredlogs.install(fmt=fmt, logger=logger, level=verboselogs.SPAM)
    elif config("LOG_LEVEL", 2, cast=int) == 1:
        coloredlogs.install(fmt=fmt, logger=logger, level=logging.DEBUG)
    elif config("LOG_LEVEL", 2, cast=int) == 2:
        coloredlogs.install(fmt=fmt, logger=logger, level=logging.INFO)
    elif config("LOG_LEVEL", 2, cast=int) == 3:
        coloredlogs.install(fmt=fmt, logger=logger, level=logging.WARNING)
    elif config("LOG_LEVEL", 2, cast=int) == 4:
        coloredlogs.install(fmt=fmt, logger=logger, level=logging.ERROR)

    return logger


def get_log_text(guild: str, user: str, message: str) -> str:
    return f"[{guild}] [{user}] {message}"
