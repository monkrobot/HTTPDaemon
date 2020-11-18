import subprocess

from sys import argv


action = argv[1]
# проверка address на соответствие адресу, если что file_name = argv[2]
address = argv[2]
file_name = argv[3]

if action == 'download':
    #subprocess.check_output([f'curl -O http://{address}/{file_name}'], shell=True)
    resp = subprocess.check_output([f'curl -O http://{address}/?filename={file_name}'], shell=True)
    print(str(resp, 'utf-8'))

if action == 'upload':
    resp = subprocess.check_output([f"curl -F 'file=@{file_name}' http://{address}/"], shell=True)
    print('file hash:', str(resp, 'utf-8'))

if action == 'delete':
    resp = subprocess.check_output([f"curl -X 'DELETE' http://{address}/?del={file_name}"], shell=True)
    print(str(resp, 'utf-8'))
