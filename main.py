import glob
import inspect
import os
import re
import sys
from functools import partial
from importlib import util
from operator import is_not

from lib.day import Day


def load_day(day: str) -> Day:
    spec = util.spec_from_file_location("model", f'days/{day}')
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name, cls in inspect.getmembers(module, inspect.isclass):
        if day.replace('.py', '').lower() == name.lower():
            return cls()


if __name__ == '__main__':
    days = filter(partial(is_not, None),
                  [load_day(file) for file in list(os.walk('days'))[0][2]
                   if re.match('day\\d+\\.py', file)])
    for day in days:
        day.run()
