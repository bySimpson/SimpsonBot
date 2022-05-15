import discord
import os # default module
from decouple import config
import inspect
import re

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