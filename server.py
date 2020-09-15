import http.server
import socketserver
import io
import cgi

from sys import argv
from urllib.parse import urlparse
from urllib.parse import parse_qs

# download curl -O http://<server_ip>:<port>/<file_name>
# upload curl -F 'file=@<file_name>' http://<server_ip>:<port>/

if argv[2:]:
    port = int(sys.argv[2])
else:
    port = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", 'application/octet-stream')

        query_components = parse_qs(urlparse(self.path).query)
        if 'delete' in query_components:
            delete = query_components['delete'][0]
            print('delete:', delete)
        else:
            self.do_POST()

    def do_POST(self):         
        r, info = self.deal_post_data()
        print('HERE IT IS')
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()      

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        print('header:', self.headers)
        print('header:', self.headers['Content-Type'])
        print('ctype, pdict:', ctype, pdict)
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            print (type(form))
            print('THIS!!!')
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open("./%s"%record.filename, "wb").write(record.file.read())
                else:
                    open("./%s"%form["file"].filename, "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded")

Handler = CustomHTTPRequestHandler
try:
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()
except OSError:
    print('Address already in use. Please change port')