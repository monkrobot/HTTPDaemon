import daemon

from sys import argv

import file_server


#with daemon.DaemonContext():
#    file_server.start_server(port=8000)
    

## Make the context manager for becoming a daemon process.
#daemon_context = daemon.DaemonContext()
##daemon_context.files_preserve = [server.fileno()]
#
## Become a daemon process.
#with daemon_context:
#    file_server.start_server()

class testDaemon(daemon.Daemon):
    def run(self):
        file_server.start_server()

server_daemon = testDaemon()

if 'start' == argv[1]: 
       daemon.start()
elif 'stop' == argv[1]: 
       daemon.stop()
elif 'restart' == argv[1]: 
       daemon.restart()

#import sys, daemon, time
#
#class testdaemon(daemon.Daemon):
#       def run(self):
#           self.i = 0
#           with open('test1.txt', 'w') as f:
#               f.write(str(self.i))
#           while True:
#               self.i += 1
#               time.sleep(1)
#
#       def quit(self):
#           with open('test2.txt', 'w') as f:
#               f.write(str(self.i))
#
#daemon = testdaemon()
#
#if 'start' == sys.argv[1]: 
#       daemon.start()
#elif 'stop' == sys.argv[1]: 
#       daemon.stop()
#elif 'restart' == sys.argv[1]: 
#       daemon.restart()