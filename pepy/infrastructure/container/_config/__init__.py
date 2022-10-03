import os
from enum import Enum, auto


class Environment(Enum):
    test = auto()
    dev = auto()
    prod = auto()


environment = Environment[os.getenv("APPLICATION_ENV", None)]

if environment == Environment.dev:
    from ._dev import *
elif environment == Environment.prod:
    from ._prod import *
elif environment == Environment.test:
    from ._test import *
else:
    raise EnvironmentError('Environment "{}" is invalid'.format(environment))
