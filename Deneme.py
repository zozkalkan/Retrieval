import os

import requests

API_TOKEN = "7733fbccdd8f6247b2c543ce68126d871170c1a5"
API_URL = "https://api.github.com/users/haciyakup/repos"

url = "{}?access_token={}".format(API_URL, API_TOKEN)
req_json = requests.get(url).json()

for repo in req_json:
    os.system("git clone {}".format(repo["git_url"]))