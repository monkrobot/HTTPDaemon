import daemon

import server

with daemon.DaemonContext():
    server.start_server(port=8000)
    