import os

port = 8080

if os.getenv('APPLICATION_ENV', None) == 'prod':
    workers = 1
    threads = 1
    timeout = 30
    capture_output = True

if os.getenv('APPLICATION_ENV', None) == 'dev':
    reload = True
    capture_output = True
