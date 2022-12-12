import argparse
import inspect
import os
import re
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
    days = sorted(filter(partial(is_not, None),
                         [load_day(file) for file in list(os.walk('days'))[0][2]
                          if re.match('day\\d+\\.py', file)]))

    parser = argparse.ArgumentParser(description='Run the Advent of Code solutions!')
    parser.add_argument('-a', action='store_true', help='Run all days')
    parser.add_argument('-d', type=int, choices=[day.get_number() for day in days],
                        help='Run a specific day')
    parser.add_argument('-l', action='store_true', help='Run the last day')
    args = parser.parse_args()

    if args.a:
        [day.run() for day in days]
    elif args.l:
        max(days).run()
    elif args.d:
        [day.run() for day in days if args.d == day.get_number()]
    else:
        [day.run() for day in days]
