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


def fetch_create_account_token():
    return fetch_tokens("createaccount")["createaccounttoken"]


def fetch_user_rights_token():
    return fetch_tokens("userrights")["userrightstoken"]


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


def change_user_group_membership(option):
    username = option["username"]

    token = option["token"]

    body = {
        "action": "userrights",
        "user": username,
        "token": token,
        "format": "json"
    }

    if "add_groups" in option:
        body["add"] = option["add_groups"]

    if "remove_groups" in option:
        body["remove"] = option["remove_groups"]

    response = session.post(url=API_ENDPOINT, data=body)

    data = response.json()

    print(data)


def add_user_to_groups(option):
    username = option["username"]
    groups = option["groups"]

    token = option["token"]

    change_user_group_membership({"username": username, "add_groups": groups, "token": token})


def create_account(option):
    username = option["username"]
    password = option["password"]
    email = option["email"]

    token = option["token"]
    return_uri = option["return_uri"]

    body = {
        "action": "createaccount",
        "username": username,
        "password": password,
        "retype": password,
        "email": email,
        "realname": "",
        "createreturnurl": return_uri,
        "createtoken": token,
        "format": "json"
    }

    response = session.post(API_ENDPOINT, data=body)

    try:
        data = response.json()

        print(data)
    except ValueError:
        print(response)
        print(response.content)


def create_accounts(option):
    accounts = option["accounts"]

    token = option["token"]
    return_uri = option["return_uri"]

    for account in accounts:
        username = account["username"]
        password = account["password"]
        email = account["email"]

        create_account({
            "username": username,
            "password": password,
            "email": email,
            "token": token,
            "return_uri": return_uri
        })


def create_bot_account(option):
    username = option["username"]
    password = option["password"]
    email = option["email"]

    create_account_token = option["create_account_token"]
    user_rights_token = option["user_rights_token"]
    return_uri = option["return_uri"]

    create_account({
        "username": username,
        "password": password,
        "email": email,
        "token": create_account_token,
        "return_uri": return_uri
    })

    add_user_to_groups({
        "username": username,
        "groups": "bot",
        "token": user_rights_token
    })


def create_bot_accounts(option):
    accounts = option["accounts"]

    create_account_token = option["create_account_token"]
    user_rights_token = option["user_rights_token"]
    return_uri = option["return_uri"]

    for account in accounts:
        username = account["username"]
        password = account["password"]
        email = account["email"]

        create_bot_account({
            "username": username,
            "password": password,
            "email": email,
            "create_account_token": create_account_token,
            "user_rights_token": user_rights_token,
            "return_uri": return_uri
        })


def main(*args):
    accounts = [
        {"username": "User1", "password": "password", "email": "user1@domain.tld"},
        {"username": "User2", "password": "password", "email": "user2@domain.tld"},
        {"username": "User3", "password": "password", "email": "user3@domain.tld"},
        {"username": "User4", "password": "password", "email": "user4@domain.tld"},
        {"username": "User5", "password": "password", "email": "user5@domain.tld"},
        {"username": "User6", "password": "password", "email": "user6@domain.tld"},
        {"username": "User7", "password": "password", "email": "user7@domain.tld"},
        {"username": "User8", "password": "password", "email": "user8@domain.tld"},
        {"username": "User9", "password": "password", "email": "user9@domain.tld"},
        {"username": "User10", "password": "password", "email": "user10@domain.tld"},
        {"username": "User10a", "password": "password", "email": "user10@domain.tld"}
    ]

    accounts = [
        {"username": "User11", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11a", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11b", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11c", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11d", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11e", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11f", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11g", "password": "password", "email": "user11@domain.tld"},
        {"username": "User11h", "password": "password", "email": "user11@domain.tld"}
    ]

    bot_accounts = [
        {"username": "FirstBot", "password": "password", "email": "firstbot@domain.tld"},
        {"username": "SecondBot", "password": "password", "email": "secondbot@domain.tld"},
        {"username": "TestBot", "password": "password", "email": "testbot@domain.tld"}
    ]

    print("Fetching login token...")
    login_token = fetch_login_token()
    print()

    print("Logging in...")
    login({"username": USERNAME, "password": PASSWORD, "token": login_token, "return_uri": WIKI_URI})
    print()

    print("Fetching create account token...")
    create_account_token = fetch_create_account_token()
    print()

    print("Creating accounts...")
    create_accounts({"accounts": accounts, "token": create_account_token, "return_uri": WIKI_URI})
    print()

    print("Fetching user rights token...")
    user_rights_token = fetch_user_rights_token()
    print()

    print("Creating bot accounts...")
    create_bot_accounts({"accounts": bot_accounts, "create_account_token": create_account_token, "user_rights_token": user_rights_token, "return_uri": WIKI_URI})


if __name__ == "__main__":
    main()