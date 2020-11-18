import requests as req

from sys import argv



action = argv[1]
address = argv[2]
filename = argv[3]

def client_func(action: str = 'download', address: str = 'localhost:8000', filename: str = None):
# download from server
    if action == 'download':
        resp = req.get(f'http://{address}/get?filename={filename}')

        if resp.status_code == 200:
            with open(f'{filename}', 'wb') as f:
                f.write(resp.content)
            return f'{filename} is downloaded'
        else:
            return resp.text


    # upload to server
    if action == 'upload':
        url = f'http://{address}/post?'

        try:
            with open(f'{filename}', 'rb') as f:
                files = {'file': f}
                resp = req.post(f'http://{address}/post?', files=files)
                return resp.text
        except FileNotFoundError:
            return('No such file')


    # delete from server
    if action == 'delete':
        resp = req.delete(f'http://{address}/delete?del={filename}')
        return resp.text


if __name__ == "__main__":
    print(client_func(action=action, address=address, filename=filename))