import os

port = 8080


if os.getenv('APPLICATION_ENV', None) == 'prod':
    workers = 2
    threads = 1
    timeout = 30
    capture_output = True
    accesslog = '-'

if os.getenv('APPLICATION_ENV', None) == 'dev':
    reload = True
    capture_output = True
