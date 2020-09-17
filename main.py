import http.server as BaseHTTPServer
import os
import shutil
import subprocess
import sys
from urllib.parse import urlparse
from urllib.parse import parse_qs

FILEPATH = sys.argv[1] if sys.argv[1:] else __file__

class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", 'application/octet-stream')
        
        file_path = FILEPATH
        #query_components = parse_qs(urlparse(self.path).query)
        #if 'hash' in query_components:
        #    hash = query_components['hash'][0]
        #    file_path = f'./{hash}'
        print(file_path)
        with open(file_path, 'rb') as f:
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(file_path)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)



            

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print('post_data:', post_data)

def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer,
         protocol="HTTP/1.0"):
    
    if sys.argv[2:]:
        port = int(sys.argv[2])
    else:
        port = 8000
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    httpd = BaseHTTPServer.HTTPServer(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on {0[0]} port {0[1]} ... {1}".format(sa, FILEPATH))

    httpd.serve_forever()



#class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
#    def do_GET(self):
#        with open(FILEPATH, 'rb') as f:
#            self.send_response(200)
#            self.send_header("Content-Type", 'application/octet-stream')
#
#            file_path = FILEPATH
#            query = parse_qs(urlparse(self.path).query)
#            if 'name' in query:
#                name = query['name'][0]
#                print('name:', name)
#
#            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
#            fs = os.fstat(f.fileno())
#            self.send_header("Content-Length", str(fs.st_size))
#            self.end_headers()
#            shutil.copyfileobj(f, self.wfile)

if __name__ == '__main__':
    test()