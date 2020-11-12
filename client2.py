import requests as req

from sys import argv


action = argv[1]
filename = argv[2]

# download from server
if action == 'download':
    resp = req.get(f'http://localhost:8000/get?filename={filename}')  # 72acded3acd45e4c8b6ed680854b8ab1

    with open(f'{filename}', 'wb') as f:
        f.write(resp.content)
    if resp.status_code == 200:
        print(f'{filename} is downloaded')
    else:
        print(resp.text)


# upload to server
if action == 'upload':
    url = 'http://localhost:8000/post?'
    print(filename)

    with open(f'{filename}', 'rb') as f:

        files = {'file': f}

        resp = req.post(url, files=files)
        print(resp.text)


# delete from server
if action == 'delete':
    resp = req.delete(f'http://localhost:8000/?del={filename}')
    print(resp.text)