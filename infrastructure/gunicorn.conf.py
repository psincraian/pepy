import os

if os.getenv('APPLICATION_ENV', None) == 'prod':
    workers = 2
    threads = 1
    timeout = 30
    daemon = True
    accesslog = '/var/log/flasky-access.log'
    loglevel = 'debug'

if os.getenv('APPLICATION_ENV', None) == 'dev':
    reload = True
    capture_output = True
