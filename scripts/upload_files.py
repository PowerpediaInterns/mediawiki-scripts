#!/usr/bin/env python
"""
Copyright 2019 David Wong

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

session = requests.Session()
session.verify = False

WIKI_URI = "https://192.168.56.56/demo"
API_ENDPOINT = WIKI_URI + "/api.php"

USERNAME = "Admin"
PASSWORD = "adminpass"


def fetch_tokens(type):
    body = {
        "action": "query",
        "meta": "tokens",
        "type": type,
        "format": "json"
    }

    response = session.get(url=API_ENDPOINT, params=body)
    data = response.json()

    tokens = data["query"]["tokens"]

    return tokens


def fetch_login_token():
    return fetch_tokens("login")["logintoken"]


def fetch_csrf_token():
    return fetch_tokens("csrf")["csrftoken"]


def login(option):
    username = option["username"]
    password = option["password"]

    token = option["token"]
    return_uri = option["return_uri"]

    body = {
        "action": "clientlogin",
        "username": username,
        "password": password,
        "loginreturnurl": return_uri,
        "logintoken": token,
        "format": "json"
    }

    response = session.post(url=API_ENDPOINT, data=body)

    data = response.json()

    print(data)


def upload_file(option):
    file_name = option["name"]
    file_data = option["data"]

    token = option["token"]

    body = {
        "action": "upload",
        "filename": file_name,
        "token": token,
        "format": "json",
        "ignorewarnings": 1
    }

    files = {
        "file": (file_name, file_data, "multipart/form-data")
    }

    response = session.post(API_ENDPOINT, files=files, data=body)

    try:
        data = response.json()

        print(data)
    except ValueError:
        print(response)
        print(response.content)


def upload_files(option):
    files = option["files"]

    token = option["token"]

    for file in files:
        name = file["name"]
        data = file["data"]

        upload_file({
            "name": name,
            "data": data,
            "token": token
        })


def create_pdf(text):
    return f"""%PDF-1.0
9 0 obj<<>>stream
BT/ 9 Tf({text})' ET
endstream
endobj 4 0 obj<</Parent 5 0 R/Contents 9 0 R>>endobj 5 0 obj<</Kids[4 0 R]/Count 1/MediaBox[0 0 99 9]>>endobj 3 0 obj<</Pages 5 0 R>>endobj trailer<</Root 3 0 R>>"""


def main(*args):
    minimal_pdf = """%PDF-1.0
1 0 obj<</Pages 2 0 R>>endobj 2 0 obj<</Kids[3 0 R]/Count 1>>endobj 3 0 obj<</MediaBox[0 0 3 3]>>endobj
trailer<</Root 1 0 R>>"""
    minimal_gif = base64.b64decode("R0lGODlhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs=")
    minimal_docx = base64.b64decode("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")

    files = [
        {"name": "Minimal PDF.pdf", "data": minimal_pdf},
        {"name": "Minimal GIF.gif", "data": minimal_gif},
        {"name": "Minimal DOCX.docx", "data": minimal_docx}
    ]

    files.extend(
        {"name": f"Minimal PDF {i}.pdf", "data": create_pdf(i)} for i in range(1, 501)
    )

    print("Fetching login token...")
    login_token = fetch_login_token()
    print()

    print("Logging in...")
    login({"username": USERNAME, "password": PASSWORD, "token": login_token, "return_uri": WIKI_URI})
    print()

    print("Fetching CSRF token...")
    csrf_token = fetch_csrf_token()
    print()

    print("Uploading files...")
    upload_files({"files": files, "token": csrf_token})


if __name__ == "__main__":
    main()