import requests as req

from sys import argv


# filename = argv[1]
# resp = req.get(f"http://localhost:8000/get?filename={filename}")  # 72acded3acd45e4c8b6ed680854b8ab1
# 
# with open(f'{filename}', 'wb') as f:
#     f.write(resp.content)
# print(resp.text)
# print(resp.content)

url = 'http://localhost:8000/post?'

filename = argv[1]
print(filename)

with open(f'{filename}', 'rb') as f:

    files = {'bytefiles': f}

    r = req.post(url, files=files)
    print(r.text)