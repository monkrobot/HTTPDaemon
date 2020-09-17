import cgi
import http.server
import io
import os
import socketserver

from pathlib import Path
import shutil
from sys import argv
from urllib.parse import urlparse
from urllib.parse import parse_qs

# download curl -O http://<server_ip>:<port>/<file_name>
# upload curl -F 'file=@<file_name>' http://<server_ip>:<port>/

FILEPATH = argv[0]

#p = Path('.')
#q = p / 'test123'
#q.mkdir()
#q.unlink()
#print(q.exists())
if argv[2:]:
    port = int(argv[2])
else:
    port = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    # This function allow client to download file
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", 'application/octet-stream')
        query_components = parse_qs(urlparse(self.path).query)
        print("query_components:", query_components)
        #file_name = ''.join(query_components['filename'])
        #print("file_name:", file_name)
        
        file_path = FILEPATH
        print(file_path)
        with open(file_path, 'rb') as f:
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(file_path)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

    # This function allow client to upload file
    def do_POST(self):
        print('HERE IT IS')         
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

    # This function allow client to delete file
    def do_DELETE(self):
        print('THIS IS DELETE')
        print('header:', self.headers)
        query_components = parse_qs(urlparse(self.path).query)
        file_name = ''.join(query_components['del'])
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            self.send_error(404)

        # ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        # pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        # if ctype == 'multipart/form-data':
        #     form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'DELETE', 'CONTENT_TYPE':self.headers['Content-Type'], })
        #     print("form:", form)

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