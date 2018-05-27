import os

environment = os.getenv('APPLICATION_ENV', None)

if environment == 'dev':
    from ._dev import *
elif environment == 'prod':
    from ._prod import *
elif environment == 'test':
    from ._test import *
else:
    raise EnvironmentError("Environment \"{}\" is invalid".format(environment))
