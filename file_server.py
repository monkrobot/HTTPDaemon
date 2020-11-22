import cgi
import hashlib
import http.server
import io
import logging
import os
import shutil
import socketserver

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from sys import argv
from urllib.parse import urlparse
from urllib.parse import parse_qs


if argv[2:]:
    port = int(argv[2])
else:
    port = 8000

#logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('TESTTTTT')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("./app.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):


    # This function allows client to download file
    def do_GET(self):
        response = io.BytesIO()
        
        query_components = parse_qs(urlparse(self.path).query)
        file_name = ''.join(query_components['filename'])
        logger.info(f'download query_components: {query_components}, file_name: {file_name}')
        
        if file_name:
            file_path = Path(f'./{file_name[0:2]}/{file_name}')
            if file_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", 'application/octet-stream')
                with open(file_path, 'rb') as f:
                    self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(file_path)))
                    fs = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    #self.end_headers()
                    #shutil.copyfileobj(f, self.wfile)
            else:
                response.write(b"No such file to download\n")
                logger.info('No such file to download')
                length = response.tell()
                response.seek(0)
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-Length", str(length))
                #self.end_headers()
            if response:
                self.end_headers()
                shutil.copyfileobj(response, self.wfile)
                response.close()
        else:
            response.write(b"To download file enter filename\n")
            length = response.tell()
            response.seek(0)
            self.send_response(404)



            

    # This function allows client to upload file
    def do_POST(self):
        resp, info, hash_filename = self.deal_post_data()
        logger.info(f'{resp}, {info}, {hash_filename}, "by: ", {self.client_address}')
        
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
            shutil.copyfileobj(response, self.wfile)
            response.close()

    # This function allows client to delete file
    def do_DELETE(self):
        query_components = parse_qs(urlparse(self.path).query)
        file_name = ''.join(query_components['del'])

        logger.info(f'delete query_components: {query_components}, file_name: {file_name}')

        file_folder = Path(f'./{file_name[0:2]}')
        file_path = file_folder / f'{file_name}'

        response = io.BytesIO()
        
        if file_path.exists():
            file_path.unlink()
            try:
                file_folder.rmdir()
            except OSError:
                print(f"{file_folder} is not empty to delete")
            
            response.write(b"File deleted\n")
            logger.info('File deleted')
            self.send_response(204)
        else:
            print("No such file\n")
            response.write(f"{query_components}\n".encode())
            #response.write(b"No such file to delete\n")
            logger.info('No such file to delete')
            self.send_response(404)

        length = response.tell()
        response.seek(0)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if response:
            shutil.copyfileobj(response, self.wfile)
            response.close()

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        logger.info(f'ctype, pdict: {ctype}, {pdict}')
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
                else:
                    open(f"./{hash_p}/{hash_filename}", "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded", hash_filename)


Handler = CustomHTTPRequestHandler

def start_server(port=8000):
    #logging.info('start server')
    logger.info('start server')
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("serving at port", port)
            #logging.info('serving at port %d' % port)
            logger.info('serving at port %d' % port)
            httpd.serve_forever()
    except OSError:
        print('Address already in use. Please change port')


if __name__ == "__main__":
    start_server(port)
