import requests as req


resp = req.get("http://localhost:8000/?filename=72acded3acd45e4c8b6ed680854b8ab1")

with open('file.jpg', 'wb') as f:
    f.write(resp.content)
#print(resp.text)
#print(resp.content)