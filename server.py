import cgi
import hashlib
import http.server
import io
import os
import shutil
import socketserver

from pathlib import Path
from sys import argv
from urllib.parse import urlparse
from urllib.parse import parse_qs

# download curl -O http://<server_ip>:<port>/?<file_name>
# upload curl -F 'file=@<file_name>' http://<server_ip>:<port>/
#curl -O http://localhost:8000/?filename=e1671797c52e15f763380b45e841ec32
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
        file_name = ''.join(query_components['filename'])
        
        file_path = Path(f'./{file_name[0:2]}/{file_name}')
        if file_path.exists():
            print(file_path)
            with open(file_path, 'rb') as f:
                self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(file_path)))
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)
        else:
            response = io.BytesIO()
            response.write(b"No such file\n")
            length = response.tell()
            response.seek(0)
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(length))
            self.end_headers()

    # This function allow client to upload file
    def do_POST(self):     
        resp, info, hash_filename = self.deal_post_data()
        print(resp, info, hash_filename, "by: ", self.client_address)
        response = io.BytesIO()
        if resp:
            response.write(f"{hash_filename}\n".encode())
        else:
            response.write(b"Failed\n")
        length = response.tell()
        response.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if response:
            self.copyfile(response, self.wfile)
            response.close()

    # This function allow client to delete file
    def do_DELETE(self):
        query_components = parse_qs(urlparse(self.path).query)
        file_name = ''.join(query_components['del'])
        file_path = Path(f'./{file_name[0:2]}/{file_name}')
        if file_path.exists():
            file_path.unlink()
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
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            
            hash_obj = hashlib.md5(form["file"].filename.encode())
            hash_filename = hash_obj.hexdigest()
            init_p = Path('.')
            hash_p = init_p / hash_filename[0:2]
            if not hash_p.exists():
                hash_p.mkdir()
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open(f"./{hash_p}/{hash_filename}", "wb").write(record.file.read())
                        #open("./%s"%record.filename, "wb").write(record.file.read())
                else:
                    open(f"./{hash_p}/{hash_filename}", "wb").write(form["file"].file.read())
                    #open("./%s"%form["file"].filename, "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded", hash_filename)

Handler = CustomHTTPRequestHandler
try:
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()
except OSError:
    print('Address already in use. Please change port')