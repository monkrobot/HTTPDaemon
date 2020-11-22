import daemon
import os
import logging
import sys

import pathlib

from sys import argv

import file_server


#with daemon.DaemonContext():
#    file_server.start_server(port=8000)
   
#sys.stdout = open('Output.txt', 'a')


working_directory = os.getcwd()
#log = open('./app.log', 'a')
#logger = logging.getLogger("DaemonLog")
#logger.setLevel(logging.INFO)
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler = logging.FileHandler("./testdaemon.log")
#handler.setFormatter(formatter)
#logger.addHandler(handler)
# Make the context manager for becoming a daemon process.
daemon_context = daemon.DaemonContext(
                                      working_directory=working_directory,
                                      files_preserve=[file_server.handler.stream],
                                      umask=0o002,
                                      stdout=sys.stdout,
                                      stderr=sys.stderr)
                                      #files_preserve=[log],
#daemon_context.files_preserve = [server.fileno()]

# Become a daemon process.
with daemon_context:

    file_server.start_server()
    print("hello there, this is daemon")
    print(os.getcwd())



# #standard python libs
# import logging
# import time
# 
# #third party libs
# from daemon import runner
# 
# class App():
#    
#        def __init__(self):
#               self.stdin_path = '/dev/null'
#               self.stdout_path = '/dev/tty'
#               self.stderr_path = '/dev/tty'
#               self.pidfile_path =  './testdaemon.pid'
#               self.pidfile_timeout = 5
# 
#            
#        def run(self):
#               while True:
#                      file_server.start_server()
#                      #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
#                      logger.debug("Debug message")
#                      logger.info("Info message")
#                      logger.warn("Warning message")
#                      logger.error("Error message")
#                      time.sleep(10)
# 
# app = App()
# logger = logging.getLogger("DaemonLog")
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler = logging.FileHandler("./testdaemon.log")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# 
# daemon_runner = runner.DaemonRunner(app)
# #This ensures that the logger file handle does not get closed during daemonization
# daemon_runner.daemon_context.files_preserve=[handler.stream]
# daemon_runner.do_action()





#import time
#from daemon import runner
#
#class App():
#    def __init__(self):
#        self.stdin_path = '/dev/null'
#        self.stdout_path = '/dev/tty'
#        self.stderr_path = '/dev/tty'
#        self.pidfile_path =  '/tmp/foo.pid'
#        self.pidfile_timeout = 5
#    def run(self):
#        while True:
#            print("Howdy!  Gig'em!  Whoop!")
#            time.sleep(10)
#
#app = App()
#daemon_runner = runner.DaemonRunner(app)
#daemon_runner.do_action()
